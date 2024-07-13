import asyncio

from adapter import console_adapter
from bot import EchoBot

# Create adapter
ADAPTER = console_adapter.ConsoleAdapter()
BOT = EchoBot()

LOOP = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        # Greet user
        print("Hi... I'm an echobot. Whatever you say I'll echo back.")

        LOOP.run_until_complete(ADAPTER.process_activity(BOT.on_turn))
    except KeyboardInterrupt:
        pass
    finally:
        LOOP.stop()
        LOOP.close()