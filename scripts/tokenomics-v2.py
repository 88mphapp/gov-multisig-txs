# brownie run scripts/tokenomics-v2.py --network mainnet-fork

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
    mph_minter_abi = [{"inputs": [{"internalType": "uint256", "name": "prod1", "type": "uint256"}], "name": "PRBMath__MulDivFixedPointOverflow", "type": "error"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": True, "internalType": "string", "name": "paramName", "type": "string"}, {"indexed": False, "internalType": "address", "name": "newValue", "type": "address"}], "name": "ESetParamAddress", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": True, "internalType": "string", "name": "paramName", "type": "string"}, {"indexed": False, "internalType": "address", "name": "pool", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "newValue", "type": "uint256"}], "name": "ESetParamUint", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "depositorReward", "type": "uint256"}], "name": "MintDepositorReward", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "funderReward", "type": "uint256"}], "name": "MintFunderReward", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"}, {"indexed": True, "internalType": "bytes32", "name": "previousAdminRole", "type": "bytes32"}, {"indexed": True, "internalType": "bytes32", "name": "newAdminRole", "type": "bytes32"}], "name": "RoleAdminChanged", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"}, {"indexed": True, "internalType": "address", "name": "account", "type": "address"}, {"indexed": True, "internalType": "address", "name": "sender", "type": "address"}], "name": "RoleGranted", "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "internalType": "bytes32", "name": "role", "type": "bytes32"}, {"indexed": True, "internalType": "address", "name": "account", "type": "address"}, {"indexed": True, "internalType": "address", "name": "sender", "type": "address"}], "name": "RoleRevoked", "type": "event"}, {"inputs": [], "name":"CONVERTER_ROLE", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"DEFAULT_ADMIN_ROLE", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"LEGACY_MINTER_ROLE", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"WHITELISTED_POOL_ROLE", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"WHITELISTER_ROLE", "outputs":[{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "converterMint", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "account", "type": "address"}, {"internalType": "uint64", "name": "depositID", "type": "uint64"}], "name": "createVestForDeposit", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"devRewardMultiplier", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"devWallet", "outputs":[{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint64", "name": "fundingID", "type": "uint64"}, {"internalType": "uint256", "name": "interestAmount", "type": "uint256"}], "name": "distributeFundingRewards", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}], "name": "getRoleAdmin", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"govRewardMultiplier", "outputs":[{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name":"govTreasury", "outputs":[{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}, {"internalType": "address", "name": "account", "type": "address"}], "name": "grantRole", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes32", "name": "role",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       "type": "bytes32"}, {"internalType": "address", "name": "account", "type": "address"}], "name": "hasRole", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_mph", "type": "address"}, {"internalType": "address", "name": "_govTreasury", "type": "address"}, {"internalType": "address", "name": "_devWallet", "type": "address"}, {"internalType": "address", "name": "_vesting02", "type": "address"}, {"internalType": "uint256", "name": "_devRewardMultiplier", "type": "uint256"}, {"internalType": "uint256", "name": "_govRewardMultiplier", "type": "uint256"}], "name": "initialize", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "pool", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "depositAmount", "type": "uint256"}, {"internalType": "uint256", "name": "fundingCreationTimestamp", "type": "uint256"}, {"internalType": "uint256", "name": "maturationTimestamp", "type": "uint256"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "bool", "name": "early", "type": "bool"}], "name": "legacyMintFunderReward", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "mintVested", "outputs": [{"internalType": "uint256", "name": "mintedAmount", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name":"mph", "outputs":[{"internalType": "contract MPHToken", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "poolDepositorRewardMintMultiplier", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "poolFunderRewardMultiplier", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}, {"internalType": "address", "name": "account", "type": "address"}], "name": "renounceRole", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes32", "name": "role", "type": "bytes32"}, {"internalType": "address", "name": "account", "type": "address"}], "name": "revokeRole", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "uint256", "name": "newMultiplier", "type": "uint256"}], "name": "setDevRewardMultiplier", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "newValue", "type": "address"}], "name": "setDevWallet", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "uint256", "name": "newMultiplier", "type": "uint256"}], "name": "setGovRewardMultiplier", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "newValue", "type": "address"}], "name": "setGovTreasury", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "newValue", "type": "address"}], "name": "setMPHTokenOwner", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"setMPHTokenOwnerToZero", "outputs":[], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "pool", "type": "address"}, {"internalType": "uint256", "name": "newMultiplier", "type": "uint256"}], "name": "setPoolDepositorRewardMintMultiplier", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "pool", "type": "address"}, {"internalType": "uint256", "name": "newMultiplier", "type": "uint256"}], "name": "setPoolFunderRewardMultiplier", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "address", "name": "newValue", "type": "address"}], "name": "setVesting02", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint64", "name": "depositID", "type": "uint64"}, {"internalType": "uint256", "name": "currentDepositAmount", "type": "uint256"}, {"internalType": "uint256", "name": "depositAmount", "type": "uint256"}], "name": "updateVestForDeposit", "outputs": [], "stateMutability":"nonpayable", "type":"function"}, {"inputs": [], "name":"vesting02", "outputs":[{"internalType": "contract Vesting02", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}]
    mph_minter = Contract.from_abi(
        "MPHMinter", "0x01C2fEe5d6e76ec26162DAAF4e336BEed01F2651", mph_minter_abi, safe.account)
    mph = safe.contract("0x8888801aF4d980682e47f1A9036e589479e835C5")
    sablier = safe.contract("0xCD18eAa163733Da39c232722cBC4E8940b1D8888")
    dev_treasury = "0xfecBad5D60725EB6fd10f8936e02fa203fd27E4b"
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
    # 10-year vests:
    # 88mph foundation: 101111.08
    # Because Sablier doesn't support streaming to oneself, the tokens are sent to
    # the dev treasury instead, which will handle creating a stream to the gov treasury

    mph.transfer(dev_treasury, (12819.44 + 101111.08) * 1e18)

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
    # Halve depositor MPH reward rates & remove yield token MPH rewards
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
            if pool_map[key]["protocol"] == "Cream":
                # cream pool, remove all depositor rewards
                mph_minter.setPoolDepositorRewardMintMultiplier(
                    pool_address, 0)
            else:
                # not cream pool, halve depositor rewards
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
