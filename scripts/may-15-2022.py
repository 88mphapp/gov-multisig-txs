# brownie run scripts/may-15-2022.py --network mainnet-fork

from ape_safe import ApeSafe

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")
    lm_pool = safe.contract("0xd48Df82a6371A9e0083FbfC0DF3AF641b8E21E44")

    ######################################################################
    # Deposit 5k MPH into Uniswap v2 LM pool as rewards
    ######################################################################

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
