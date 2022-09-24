# brownie run scripts/sep-24-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie

def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")

    ######################################################################
    # Schedule Vesting upgrade
    ######################################################################

    vesting_proxy = "0xA907C7c3D13248F08A3fb52BeB6D1C079507Eb4B"
    new_vesting_implementation = "0xEEd19eE47C820543d43C68Fa793620428C5B284a"
    default_proxy_admin = safe.contract("0x9cE2Eb5871ADF6444004C3182960A4f5dB908545")
    timelock_tx_data = default_proxy_admin.upgrade.encode_input(vesting_proxy, new_vesting_implementation)
    timelock = safe.contract("0x90523c113517A59f6BEBC123b75612Aea9FD3140")
    timelock.schedule(default_proxy_admin.address, 0, timelock_tx_data, brownie.convert.to_bytes(0), brownie.convert.to_bytes(0), 172800)

    ######################################################################
    # Submit transaction to Gnosis Safe
    ######################################################################

    # generate safe tx
    safe_tx = safe.multisend_from_receipts()

    # sign safe tx
    safe.sign_with_frame(safe_tx).hex()

    # post tx
    safe.post_transaction(safe_tx)
