# brownie run scripts/oct-4-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie


def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")

    # read pools
    with open('scripts/pools.json', 'r') as f:
        data = f.read()
    pool_map = json.loads(data)["1"]
    pool_keys = pool_map.keys()

    ######################################################################
    # Transfer MPH to GaugeRewardsDistributor
    ######################################################################

    mph = safe.contract("0x8888801aF4d980682e47f1A9036e589479e835C5")
    gauge_rewards_distributor = safe.contract("0x362A1844be1209073Fa31561c5c1d6D893255B42")
    mph.transfer(gauge_rewards_distributor.address, 4000 * 1e18) # 4 weeks of rewards, 1k MPH per week

    ######################################################################
    # Distribute reward to all gauges (Forwarder contracts)
    ######################################################################

    vesting_proxy = "0xA907C7c3D13248F08A3fb52BeB6D1C079507Eb4B"
    with open('scripts/abi/Vesting03.json') as f:
        abi = json.loads(f.read())
    vesting_contract = Contract.from_abi(
        "Vesting03", vesting_proxy, abi, safe.account)

    for key in pool_keys:
        if pool_map[key]["protocol"] == "Cream":
            # skip all cream pools
            continue
        pool_address = pool_map[key]["address"]
        forwarder_address = vesting_contract.forwarderOfPool(pool_address)

        if gauge_rewards_distributor.currentReward(forwarder_address) > 0:
            # distribute reward to forwarder
            gauge_rewards_distributor.distributeReward(forwarder_address)

            # distribute the forwarder's balance to vesting
            forwarder_balance = mph.balanceOf(forwarder_address)
            if forwarder_balance > 0:
                vesting_contract.notifyRewardAmount(pool_address, forwarder_balance)

    ######################################################################
    # Submit transaction to Gnosis Safe
    ######################################################################

    # generate safe tx
    safe_tx = safe.multisend_from_receipts()

    # sign safe tx
    safe.sign_with_frame(safe_tx).hex()

    # post tx
    safe.post_transaction(safe_tx)
