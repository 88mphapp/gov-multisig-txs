# brownie run scripts/mar-3-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")

    ######################################################################
    # Execute Dumper upgrade
    ######################################################################

    dumper_proxy = "0x8Cc9ADF88fe0b5C739bD936E9edaAd30578f4265"
    new_dumper_implementation = "0xF7d3135d5cFF29AB5cdd8644AA1e2e7566619555"
    default_proxy_admin = safe.contract("0x9cE2Eb5871ADF6444004C3182960A4f5dB908545")
    timelock_tx_data = default_proxy_admin.upgrade.encode_input(dumper_proxy, new_dumper_implementation)
    timelock = safe.contract("0x90523c113517A59f6BEBC123b75612Aea9FD3140")
    timelock.execute(default_proxy_admin.address, 0, timelock_tx_data, brownie.convert.to_bytes(0), brownie.convert.to_bytes(0))

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
