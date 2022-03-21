import asyncio
from app import Log
from app.tasks import start


if __name__ == "__main__":
    # Start background manager
    scheduler = start()
    Log.info(f"STARTING: Burn Async Scheduler")
    asyncio.get_event_loop().run_forever()
