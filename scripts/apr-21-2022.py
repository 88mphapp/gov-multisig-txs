# brownie run scripts/apr-21-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")
    bancor = safe.contract("0x853c2D147a1BD7edA8FE0f58fb3C5294dB07220e")
    bancor_mph_dstoken = "0xAbf26410b1cfF45641aF087eE939E52e328ceE46"
    mph = safe.contract("0x8888801aF4d980682e47f1A9036e589479e835C5")
    lm_pool = safe.contract("0xd48Df82a6371A9e0083FbfC0DF3AF641b8E21E44")

    ######################################################################
    # Deposit 30k MPH as Bancor v2 liquidity
    ######################################################################

    bancor_liquidity_amount = 30000 * 1e18
    mph.approve(bancor.address, bancor_liquidity_amount)
    bancor.addLiquidity(bancor_mph_dstoken, mph.address, bancor_liquidity_amount)

    ######################################################################
    # Deposit 5k MPH into Uniswap v2 LM pool as rewards
    ######################################################################

    mph.transfer(lm_pool.address, 5000 * 1e18)
    lm_pool.notifyRewardAmount(2500 * 1e18) # only notify half because the 5k is for 1 month and the LM pool period is 14 days

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
