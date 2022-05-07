# brownie run scripts/may-6-2022.py --network mainnet-fork

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

    fee = 0
    feemodel.overrideEarlyWithdrawFeeForDeposit("0x572bE575D1aA1Ca84d8Ac4274067f7bCB578a368", 98, fee)
    feemodel.overrideEarlyWithdrawFeeForDeposit("0x5dda04b2BDBBc3FcFb9B60cd9eBFd1b27f1A4fE3", 53, fee)
    feemodel.overrideEarlyWithdrawFeeForDeposit("0xc1F147DB2b6a9c9FbF322fAC3D1Fbf8B8aAEec10", 2, fee)
    feemodel.overrideEarlyWithdrawFeeForDeposit("0x1821aadB9AC1b7E4D56C728aFDaDc7541a785Cd2", 7, fee)


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
