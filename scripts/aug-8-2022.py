# brownie run scripts/aug-8-2022.py --network mainnet-fork

from ape_safe import ApeSafe
import json
from brownie import Contract
import brownie


def main():
    # configs
    safe = ApeSafe("0x56f34826Cc63151f74FA8f701E4f73C5EAae52AD")

    # read pools
    with open('scripts/pools.json', 'r') as f:
        data = f.read()
    pool_map = json.loads(data)["1"]
    pool_keys = pool_map.keys()

    ######################################################################
    # Execute Vesting upgrade
    ######################################################################

    vesting_proxy = "0xA907C7c3D13248F08A3fb52BeB6D1C079507Eb4B"
    new_vesting_implementation = "0x6A5aD7216e11157eB0Fb26174196B06AbB3859f4"
    default_proxy_admin = safe.contract(
        "0x9cE2Eb5871ADF6444004C3182960A4f5dB908545")
    timelock_tx_data = default_proxy_admin.upgrade.encode_input(
        vesting_proxy, new_vesting_implementation)
    timelock = safe.contract("0x90523c113517A59f6BEBC123b75612Aea9FD3140")
    timelock.execute(default_proxy_admin.address, 0, timelock_tx_data,
                     brownie.convert.to_bytes(0), brownie.convert.to_bytes(0))

    ######################################################################
    # Add gauges to GaugeController
    ######################################################################

    with open('scripts/abi/Vesting03.json') as f:
        abi = json.loads(f.read())
    vesting_contract = Contract.from_abi(
        "Vesting03", vesting_proxy, abi, safe.account)
    with open('scripts/abi/GaugeController.json') as f:
        abi = json.loads(f.read())
    gauge_controller = Contract.from_abi(
        "GaugeController", "0x16dff045De4421E836A42FC2e98d4Ec9015bd470", abi, safe.account)

    # add initial gauge type & weight
    gauge_controller.add_type("Ethereum", 1)

    # add the forwarder of each pool as a gauge
    for key in pool_keys:
        pool_address = pool_map[key]["address"]
        forwarder_address = vesting_contract.forwarderOfPool(pool_address)

        vesting_contract.deployForwarderOfPool(pool_address)
        gauge_controller.add_gauge(forwarder_address, 0, 0)

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
