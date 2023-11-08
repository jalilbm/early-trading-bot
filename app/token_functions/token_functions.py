import traceback
from web3 import Web3
from decouple import config
import asyncio
import app.bot.telegram_bot as telegram_bot
import app.utils as utils


# # Connect to Sepolia testnet
# w3 = Web3(Web3.HTTPProvider(config("ALCHEMY_SEPOLIA_URL")))

# Connect to ETH main net
w3 = Web3(Web3.HTTPProvider(config("ALCHEMY_ETH_MAIN_NET_URL")))

# Ensure that you are connected to the network
assert w3.is_connected(), "Web3 is not connected to the Ethereum network."


def sc_is_renounced(event_filter):
    for event in event_filter.get_new_entries():
        # Handle the event (event['args'] contains the data)
        if event["args"]["newOwner"] == "0x0000000000000000000000000000000000000000":
            return True
    return False


def transfer_event(event_filter):
    print("+++++++++++++++++++++++++")
    new_entries = event_filter.get_new_entries()
    print("sssssssssssssss", new_entries)

    return len(new_entries) > 0


def get_event_and_function(event_to_monitor, contract):
    match (event_to_monitor):
        case "sc_is_renounced":
            return {
                "event": contract.events.OwnershipTransferred,
                "function": sc_is_renounced,
            }
        case "Transfer":
            return {
                "event": contract.events.Transfer,
                "function": transfer_event,
            }
        case _:
            return {
                "event": None,
                "function": None,
            }


async def monitor_token_events(token, initial_delay=0):
    await asyncio.sleep(initial_delay)
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token.address), abi=token.abi
    )
    event_and_function = get_event_and_function(token.monitor_event, contract)

    event_filter = event_and_function["event"]().create_filter(fromBlock="latest")
    if not event_filter:
        return
    while True:
        try:
            if event_and_function["function"](event_filter):
                token_details = utils.get_token_details(token)
                print(token_details)
                message = utils.format_token_details(token_details, token.monitor_event)
                await telegram_bot.send_message(message)
            await asyncio.sleep(10)
        except Exception as e:
            print(traceback.format_exc())
            print(f"An error occurred while monitoring {token.name}: {e}")
