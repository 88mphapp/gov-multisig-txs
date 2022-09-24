# brownie run scripts/distribute-gauge-rewards.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie


def main():
    # configs
    safe = ApeSafe("0xfecBad5D60725EB6fd10f8936e02fa203fd27E4b")

    # read pools
    with open('scripts/pools.json', 'r') as f:
        data = f.read()
    pool_map = json.loads(data)["1"]
    pool_keys = pool_map.keys()

    ######################################################################
    # Distribute reward to all gauges (Forwarder contracts)
    ######################################################################

    mph = safe.contract("0x8888801aF4d980682e47f1A9036e589479e835C5")
    gauge_rewards_distributor = safe.contract(
        "0x362A1844be1209073Fa31561c5c1d6D893255B42")
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
                vesting_contract.notifyRewardAmount(
                    pool_address, forwarder_balance)

    ######################################################################
    # Submit transaction to Gnosis Safe
    ######################################################################

    # generate safe tx
    safe_tx = safe.multisend_from_receipts()

    # sign safe tx
    safe.sign_with_frame(safe_tx).hex()

    # post tx
    safe.post_transaction(safe_tx)
