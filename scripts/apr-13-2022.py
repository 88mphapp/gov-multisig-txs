# brownie run scripts/apr-13-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")
    with open('scripts/abi/PercentageFeeModel.json') as f:
        feemodel_abi = json.loads(f.read())
    feemodel = Contract.from_abi(
        "PercentageFeeModel", "0x9c2ae492ec3A49c769bABffC9500256749404f8E", feemodel_abi, safe.account)

    ######################################################################
    # Set early withdraw fee of deposit to 0
    ######################################################################

    pool = "0x60F0f24b0fBf066e877C3A89014c2e4E98C33678"
    depositId = 9
    fee = 0
    feemodel.overrideEarlyWithdrawFeeForDeposit(pool, depositId, fee)

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
