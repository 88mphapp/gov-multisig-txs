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
    mint_total = (246913.26 + 21666.67 + 28888.89 + 72222.20 + 12819.44 +
                  101111.08 + 231111.04 + 231111.04 + 36111.10 + 7222.22 + 116097.19) * 1e18

    ######################################################################
    # Mint MPH
    ######################################################################

    # grant converter role to gov multisig to get minting rights
    mph_minter.grantRole(converter_role, safe.address)

    # mint MPH
    mph_minter.converterMint(safe.address, mint_total)

    # keep MPH in gov treasury
    # this includes:
    # 2022 user incentives: 246913.26
    # Bug bounties: 21666.67
    # Strategic MPH sale: 28888.89
    # Protocol-owned liquidity: 72222.20

    # send MPH to dev treasury
    # this includes:
    # 88mph SA immediate unlock: 12819.44
    mph.transfer(dev_treasury, 12819.44 * 1e18)

    # 10-year vests:
    # 88mph foundation: 101111.08
    # Because Sablier doesn't support streaming to oneself, the tokens are sent to
    # a discretionary multisig, which will handle creating a stream to the gov treasury
    mph.transfer(discretionary_fund, 101111.08 * 1e18)

    # stream MPH using Sablier
    # this includes:
    #
    # 4-year vests:
    # Zefram: 231111.04
    # Guillaume: 231111.04
    # Szeth: 36111.10
    # Mathieu: 7222.22
    # 88mph SA: 116097.19

    stream_total = (231111.04 + 231111.04 + 36111.10 +
                    7222.22 + 116097.19) * 1e18
    current_time = math.floor(time.time()) + 60 * 60  # one hour in the future
    four_years = 4 * 365 * 24 * 60 * 60

    mph.approve(sablier.address, stream_total)

    sablier.createStream("0x5f350bF5feE8e254D6077f8661E9C7B83a30364e",
                         round_amount_using_duration(231111.04 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0xAfD5f60aA8eb4F488eAA0eF98c1C5B0645D9A0A0",
                         round_amount_using_duration(231111.04 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0x1bfD64aB61EACf714B2Aa37347057203f3AcA71f",
                         round_amount_using_duration(36111.10 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream("0xEF7F2e81EA14538858d962df34eB1bFDa83da395",
                         round_amount_using_duration(7222.22 * 1e18, four_years), mph.address, current_time, current_time + four_years)
    sablier.createStream(dev_treasury, round_amount_using_duration(116097.19 * 1e18, four_years),
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
