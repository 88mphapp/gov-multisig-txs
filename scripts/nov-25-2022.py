# brownie run scripts/nov-25-2022.py --network mainnet-fork

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
    # Set early withdraw fee of deposits to 0
    ######################################################################

    deposits = [
        { "pool": "0xaE5ddE7EA5c44b38c0bCcfb985c40006ED744EA6", "id": 90 },
        { "pool": "0xA0E78812E9cD3E754a83bbd74A3F1579b50436E8", "id": 20 },
        { "pool": "0x5dda04b2BDBBc3FcFb9B60cd9eBFd1b27f1A4fE3", "id": 64 }
    ]
    for deposit in deposits:
        feemodel.overrideEarlyWithdrawFeeForDeposit(deposit["pool"], deposit["id"], 0)

    ######################################################################
    # Submit transaction to Gnosis Safe
    ######################################################################

    # generate safe tx
    safe_tx = safe.multisend_from_receipts()

    # sign safe tx
    safe.sign_with_frame(safe_tx).hex()

    # post tx
    safe.post_transaction(safe_tx)
