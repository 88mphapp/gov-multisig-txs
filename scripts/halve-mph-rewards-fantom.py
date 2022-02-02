# brownie run scripts/halve-mph-rewards-fantom.py --network ftm-main-fork

from ape_safe import ApeSafe
import json
from brownie import Contract


def main():
    # configs
    safe = ApeSafe("0x916e78f904B5e854DB0578646AA182C0AAbED8C8")
    with open('scripts/abi/MPHMinter.json') as f:
        mph_minter_abi = json.loads(f.read())
    mph_minter = Contract.from_abi(
        "MPHMinter", "0xf6402B18F9494D54FcC0ee75460Bd791C9DA354c", mph_minter_abi, safe.account)

    ######################################################################
    # Halve depositor MPH reward rates & remove yield token MPH rewards
    ######################################################################

    # read pools
    with open('scripts/pools.json', 'r') as f:
        data = f.read()
    pool_map = json.loads(data)["250"]
    pool_keys = pool_map.keys()

    # set rates
    for key in pool_keys:
        pool_address = pool_map[key]["address"]

        # update depositor reward
        current_depositor_reward_multiplier = mph_minter.poolDepositorRewardMintMultiplier(
            pool_address)
        if current_depositor_reward_multiplier > 0:
            # halve depositor rewards
            mph_minter.setPoolDepositorRewardMintMultiplier(
                pool_address, current_depositor_reward_multiplier // 2)

        # update funder reward
        current_funder_reward_multiplier = mph_minter.poolFunderRewardMultiplier(
            pool_address)
        if current_funder_reward_multiplier > 0:
            mph_minter.setPoolFunderRewardMultiplier(pool_address, 0)

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
