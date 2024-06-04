import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router


logging.basicConfig(level=logging.INFO)
with open('./setting.txt','r') as f:
    API_TOKEN = f.readline()[:-1]


bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

                
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')