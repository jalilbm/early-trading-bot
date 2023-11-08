import traceback
from telegram import Bot
from decouple import config
from telegram.constants import ParseMode

# Initialize the bot with your token
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
IDS_TO_RECEIVE_BUY_SIGNAL = config("IDS_TO_RECEIVE_BUY_SIGNAL").split(",")

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message(message):
    for user_id in IDS_TO_RECEIVE_BUY_SIGNAL:
        try:
            await bot.send_message(
                chat_id=user_id, text=message, parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(traceback.format_exc())
            print(message)
            print(f"An error occurred: {e}")
