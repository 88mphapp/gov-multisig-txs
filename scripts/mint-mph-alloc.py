# brownie run scripts/mint-mph-alloc.py --network mainnet-fork

from ape_safe import ApeSafe
import time
import math
import json
from brownie import Contract


def round_amount_using_duration(amount, duration):
    amount = int(amount)
    return amount - (amount % duration)


def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")
    with open('scripts/abi/MPHMinter.json') as f:
        mph_minter_abi = json.loads(f.read())
    mph_minter = Contract.from_abi(
        "MPHMinter", "0x01C2fEe5d6e76ec26162DAAF4e336BEed01F2651", mph_minter_abi, safe.account)
    mph = safe.contract("0x8888801aF4d980682e47f1A9036e589479e835C5")
    sablier = safe.contract("0xCD18eAa163733Da39c232722cBC4E8940b1D8888")
    dev_treasury = "0xfecBad5D60725EB6fd10f8936e02fa203fd27E4b"
    discretionary_fund = "0xA9B2a4F90d0eC7A7907C11e2a17eF345d04747bF"
    converter_role = 0x1cf336fddcc7dc48127faf7a5b80ee54fce73ef647eecd31c24bb6cce3ac3eef
    mint_total = (237291.90 + 20822.39 + 27763.18 + 69407.95 + 12319.91 +
                  97171.13 + 222105.44 + 222105.44 + 34703.98 + 6940.80 + 111573.28) * 1e18

    ######################################################################
    # Mint MPH
    ######################################################################

    # grant converter role to gov multisig to get minting rights
    mph_minter.grantRole(converter_role, safe.address)

    # mint MPH
    mph_minter.converterMint(safe.address, mint_total)

    # keep MPH in gov treasury
    # this includes:
    # 2022 user incentives: 237291.90
    # Bug bounties: 20822.39
    # Strategic MPH sale: 27763.18
    # Protocol-owned liquidity: 69407.95

    # send MPH to dev treasury
    # this includes:
    # 88mph SA immediate unlock: 12319.91
    mph.transfer(dev_treasury, 12319.91 * 1e18)

    # 10-year vests:
    # 88mph foundation: 97171.13
    # Because Sablier doesn't support streaming to oneself, the tokens are sent to
    # a discretionary multisig, which will handle creating a stream to the gov treasury
    mph.transfer(discretionary_fund, 97171.13 * 1e18)

    # stream MPH using Sablier
    # this includes:
    #
    # 4-year vests:
    # Zefram: 222105.44
    # Guillaume: 222105.44
    # Szeth: 34703.98
    # Mathieu: 6940.80
    # 88mph SA: 111573.28

    stream_total = (222105.44 + 222105.44 + 34703.98 +
                    6940.80 + 111573.28) * 1e18
    current_time = math.floor(time.time()) + 5 * 24 * 60 * 60  # 5 days in the future
    four_years = 4 * 365 * 24 * 60 * 60

    mph.approve(sablier.address, stream_total)

    sablier.createStream("0x5f350bF5feE8e254D6077f8661E9C7B83a30364e",
                         round_amount_using_duration(222105.44 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0xAfD5f60aA8eb4F488eAA0eF98c1C5B0645D9A0A0",
                         round_amount_using_duration(222105.44 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0x1bfD64aB61EACf714B2Aa37347057203f3AcA71f",
                         round_amount_using_duration(34703.98 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0xEF7F2e81EA14538858d962df34eB1bFDa83da395",
                         round_amount_using_duration(6940.80 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream(dev_treasury, round_amount_using_duration(111573.28 * 1e18, four_years),
                         mph.address, current_time, current_time + four_years)

    # revoke converter role
    mph_minter.revokeRole(converter_role, safe.address)

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
