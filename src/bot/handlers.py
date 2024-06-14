import logging
import json
from datetime import datetime, timezone
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from src.bot.states import MyStates
from src.bot.utils import DataAggregator
from motor.motor_asyncio import AsyncIOMotorCollection

logger = logging.getLogger(__name__)


class BotHandlers:
    def __init__(
            self,
            bot: Bot,
            users: AsyncIOMotorCollection,
            data_collection: AsyncIOMotorCollection
    ) -> None:
        self.bot = bot
        self.users = users
        self.data_collection = data_collection
        self.data_aggregator = DataAggregator(self.data_collection)

    async def start(
            self,
            message: Message,
            state: FSMContext
    ) -> None:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        logger.info(f"Received /start command from user: {user_name}")
        try:
            await self.users.insert_one({
                "_id": user_id,
                "name": user_name,
                "created_at": datetime.now(timezone.utc)
            })
        except Exception as e:
            logger.error(f"Error inserting user: {e}")
        await message.answer(f"Привет, {user_name}!")
        await state.set_state(MyStates.waiting_for_json)

    async def get_json(
            self,
            message: Message,
            state: FSMContext
    ) -> None:
        logger.info(f"Received JSON message: {message.text}")
        try:
            received_json = json.loads(message.text)
            dt_from = datetime.fromisoformat(received_json['dt_from'])
            dt_upto = datetime.fromisoformat(received_json['dt_upto'])
            group_type = received_json['group_type']
            logger.info(f"Parsed JSON with dt_from: {dt_from}, dt_upto: {dt_upto}, group_type: {group_type}")
            answer = await self.data_aggregator.get_aggregated_data(dt_from, dt_upto, group_type)
            await message.answer(json.dumps(answer))
            logger.info(f"Sent answer: {json.dumps(answer)}")
        except (
                ValueError,
                TypeError,
                KeyError
        ) as e:
            error_message = ('Невалидный запрос. Пример запроса:\n {"dt_from": "2022-09-01T00:00:00", "dt_upto": '
                             '"2022-12-31T23:59:00", "group_type": "month"}')
            await message.answer(error_message)
            logger.error(f"Error processing message: {e}")


def setup_handlers(
        dp: Dispatcher,
        bot: Bot,
        users: AsyncIOMotorCollection,
        data_collection: AsyncIOMotorCollection
) -> None:
    handlers = BotHandlers(
        bot,
        users,
        data_collection
    )
    dp.message.register(
        handlers.start,
        Command(commands=["start"])
    )
    dp.message.register(
        handlers.get_json,
        MyStates.waiting_for_json
    )
