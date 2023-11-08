import asyncio
from rich import print
import app.utils as utils
import app.token_functions.token_functions as token_functions
import app.bot.telegram_bot as telegram_bot
from app import create_app

# Initialize the application
create_app()


async def monitor_tokens():
    tasks = []
    delay = 0
    for token in utils.get_all_tokens():
        print("--------------------------------", token.name)
        task = asyncio.create_task(token_functions.monitor_token_events(token, delay))
        tasks.append(task)
        delay += 1
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        # Create a new user instance
        # utils.save_token(
        #     address="0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
        #     chain_id=1,
        #     monitor_event="Transfer",
        # )
        loop.run_until_complete(monitor_tokens())
    finally:
        loop.close()
