import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.config.base import settings
from src.db import get_db_collections
from src.bot.handlers import setup_handlers


class TelegramBotApp:
    def __init__(self):
        self.bot = Bot(token=settings.TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db, self.users_collection, self.data_collection = get_db_collections()

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    async def start(self):
        setup_handlers(self.dp, self.bot, self.users_collection, self.data_collection)
        self.logger.info("Starting bot polling...")
        await self.dp.start_polling(self.bot)


if __name__ == '__main__':
    import asyncio

    app = TelegramBotApp()
    app.logger.info("Bot is starting...")
    asyncio.run(app.start())
