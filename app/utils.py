from decouple import config
from etherscan.contracts import Contract
from app.database import SessionLocal
import app.models as models
from app.honeypot_is import honeypot_is
from rich import print


ETHERSCAN_API_KEY = config("ETHERSCAN_API_KEY")
db_session = SessionLocal()


def get_token_abi(token_address):
    token_api = Contract(address=token_address, api_key=ETHERSCAN_API_KEY)
    return token_api.get_abi()


def get_token_name(token_address):
    token_api = Contract(address=token_address, api_key=ETHERSCAN_API_KEY)
    return token_api.get_abi()


def get_token_name(token_address):
    token_api = Contract(address=token_address, api_key=ETHERSCAN_API_KEY)
    return token_api.get_abi()


def save_token(address, chain_id, monitor_event, trading_enabled=False):
    pair_address = honeypot_is.get_token_pair(address, chain_id)
    token_details = honeypot_is.get_token_details(address, pair_address, chain_id)
    # Create a new token instance
    new_token = models.Token(
        name=token_details["token"]["name"],
        address=address,
        trade_enabled=trading_enabled,
        abi=get_token_abi(address),
        chain_id=chain_id,
        pair_address=pair_address,
        monitor_event=monitor_event,
    )

    # Add the new token to the session and commit it
    db_session.add(new_token)
    try:
        db_session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def get_token_details(token_object):
    return {
        "token": {
            "name": token_object.name,
            "address": token_object.address,
            "trade_enabled": token_object.trade_enabled,
        },
        **honeypot_is.get_token_details(
            token_object.address, token_object.pair_address, token_object.chain_id
        ),
    }


def get_all_tokens():
    # Query the database to find all tokens
    return db_session.query(models.Token).all()


def format_token_details(token_details, token_sc_renounced):
    # Emoji constants
    checkmark_emoji = "✅"
    crossmark_emoji = "❌"
    money_bag_emoji = "💰"
    chart_emoji = "📈"
    honey_emoji = "🍯"
    green_circle_emoji = "🟢"
    red_circle_emoji = "🔴"

    # Start with the renounced status
    renounced_status = checkmark_emoji if token_sc_renounced else crossmark_emoji
    formatted_message = (
        f"{renounced_status} Smart Contract Event: {token_sc_renounced}\n\n"
    )

    # Add token details
    formatted_message += (
        f"Name: {token_details['token']['name']} ({token_details['token']['symbol']})\n"
    )
    formatted_message += f"Address: `{token_details['token']['address']}`\n"
    formatted_message += f"Decimals: {token_details['token']['decimals']}\n\n"

    # Add holder details
    formatted_message += f"Holders: {token_details['holders'].get('number_of_holders')} (Successful: {token_details['holders'].get('number_of_successful_holders')})\n"
    formatted_message += f"Average Tax: `{token_details['holders'].get('average_tax') * 100 if token_details['holders'].get('average_tax') else None}%`\n"
    formatted_message += f"Highest Tax: `{token_details['holders'].get('highest_tax') * 100 if token_details['holders'].get('highest_tax') else None}%`\n\n"

    # Add pair details
    formatted_message += f"{chart_emoji} Pair: {token_details['pair']['pair_name']}\n"
    formatted_message += f"Address: `{token_details['pair']['pair_address']}`\n"
    formatted_message += f"Type: {token_details['pair']['pair_type']}\n"
    formatted_message += f"Chain: {token_details['pair']['chain']}\n"
    formatted_message += f"Created: {token_details['pair']['creation_datetime']}\n"
    formatted_message += (
        f"Liquidity: {money_bag_emoji} `{token_details['pair']['liquidity']}`\n\n"
    )

    # Add honeypot status
    honeypot_status = (
        red_circle_emoji if token_details["is_honeypot"] else green_circle_emoji
    )
    formatted_message += f"Honeypot Status: {honeypot_status} {honey_emoji}\n\n"

    # Add tax details with color
    buy_tax_color = "🔵" if token_details["taxes"]["buy_tax"] == 0 else "🔴"
    sell_tax_color = "🔵" if token_details["taxes"]["sell_tax"] == 0 else "🔴"
    formatted_message += (
        f"Buy Tax: {buy_tax_color} `{token_details['taxes']['buy_tax'] * 100}%`\n"
    )
    formatted_message += (
        f"Sell Tax: {sell_tax_color} `{token_details['taxes']['sell_tax'] * 100}%`\n"
    )
    formatted_message += f"Buy Gas: `{token_details['taxes']['buy_gas']}`\n"
    formatted_message += f"Sell Gas: `{token_details['taxes']['sell_gas']}`\n"

    return formatted_message
