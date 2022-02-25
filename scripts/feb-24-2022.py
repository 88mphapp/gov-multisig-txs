# brownie run scripts/feb-24-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")
    with open('scripts/abi/MPHMinter.json') as f:
        mph_minter_abi = json.loads(f.read())
    mph_minter = Contract.from_abi(
        "MPHMinter", "0x01C2fEe5d6e76ec26162DAAF4e336BEed01F2651", mph_minter_abi, safe.account)

    ######################################################################
    # Halve depositor MPH reward rates
    ######################################################################

    # read pools
    with open('scripts/pools.json', 'r') as f:
        data = f.read()
    pool_map = json.loads(data)["1"]
    pool_keys = pool_map.keys()

    # set rates
    for key in pool_keys:
        pool_address = pool_map[key]["address"]

        # update depositor reward
        current_depositor_reward_multiplier = mph_minter.poolDepositorRewardMintMultiplier(
            pool_address)
        if current_depositor_reward_multiplier > 0:
            mph_minter.setPoolDepositorRewardMintMultiplier(
                pool_address, current_depositor_reward_multiplier // 2)

    ######################################################################
    # Update xMPH period to 30 days
    ######################################################################

    xmph = safe.contract("0x1702F18c1173b791900F81EbaE59B908Da8F689b")
    xmph.setRewardUnlockPeriod(30 * 24 * 60 * 60)

    ######################################################################
    # Schedule Dumper upgrade
    ######################################################################

    dumper_proxy = "0x8Cc9ADF88fe0b5C739bD936E9edaAd30578f4265"
    new_dumper_implementation = "0xF7d3135d5cFF29AB5cdd8644AA1e2e7566619555"
    default_proxy_admin = safe.contract("0x9cE2Eb5871ADF6444004C3182960A4f5dB908545")
    timelock_tx_data = default_proxy_admin.upgrade.encode_input(dumper_proxy, new_dumper_implementation)
    timelock = safe.contract("0x90523c113517A59f6BEBC123b75612Aea9FD3140")
    timelock.schedule(default_proxy_admin.address, 0, timelock_tx_data, brownie.convert.to_bytes(0), brownie.convert.to_bytes(0), 172800)

    ######################################################################
    # Submit transaction to Gnosis Safe
    ######################################################################

    # generate safe tx
    safe_tx = safe.multisend_from_receipts()
    safe.preview(safe_tx)

    # sign safe tx
    safe.sign_with_frame(safe_tx).hex()

    # post tx
    safe.post_transaction(safe_tx)
