import asyncio
from decouple import config
from telethon import TelegramClient, events
from rich import print

TELETHON_ID = config("TELETHON_ID")
TELETHON_HASH = config("TELETHON_HASH")
PROFICY_PRICE_BOT_USERNAME = "ProficyPriceBot"

# Initialize the Telegram client
client = TelegramClient("earlyTrader", TELETHON_ID, TELETHON_HASH)


def get_tax_from_proficy_price_bot_message(message):
    tax = message.split("**Tax:**")[1].split("|")[0]
    return {
        "buy_tax": float(tax.split("/")[0].strip()),
        "sell_tax": float(tax.split("/")[1].strip()),
    }


# Listen for the response
@client.on(events.NewMessage(chats=PROFICY_PRICE_BOT_USERNAME))
async def handler(event):
    a = event.message.text
    print("Bot responded:\n", a)
    print(get_tax_from_proficy_price_bot_message(a))


async def get_proficy_price_bot_price_details(token_address):
    await client.send_message(PROFICY_PRICE_BOT_USERNAME, f"/p {token_address}")


async def main():
    await client.start()
    await get_proficy_price_bot_price_details(
        "0xd01273eff030b1cbe87f54b35da48ffd4e37d011"
    )
    # Wait for a while to let the bot respond
    await asyncio.sleep(10)  # Adjust the sleep time as needed
    await client.disconnect()


# Run the client
client.loop.run_until_complete(main())
