import sys
import pytest
from unittest.mock import AsyncMock, patch, ANY, MagicMock
from aiogram.types import Message, User, Chat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher

motor_asyncio_patch = MagicMock()
motor_asyncio_patch.platform_info.return_value = 'Python/AsyncIO'
sys.modules['motor.frameworks.asyncio'] = motor_asyncio_patch

from src.bot.handlers import BotHandlers
from src.config.base import settings


@pytest.fixture
def bot():
    return Bot(token=settings.TOKEN)


@pytest.fixture
def dispatcher(
        bot
):
    dispatcher = Dispatcher()
    dispatcher['bot'] = bot
    dispatcher['storage'] = MemoryStorage()
    return dispatcher


@pytest.fixture
def db_collections():
    users_collection = MagicMock(
        name='users'
    )
    data_collection = MagicMock(
        name='data_collection'
    )
    return {
        'users': users_collection,
        'data_collection': data_collection
    }


@pytest.fixture
def handlers(
        bot,
        db_collections
):
    users = db_collections['users']
    data_collection = db_collections['data_collection']
    return BotHandlers(bot, users, data_collection)


@pytest.mark.asyncio
async def test_start_handler(
        handlers,
        dispatcher
):
    user_id = 123
    user_name = "TestUser"
    user = User(
        id=user_id,
        is_bot=False,
        first_name=user_name
    )
    chat = Chat(
        id=user_id,
        type="private"
    )

    message = MagicMock(
        spec=Message
    )
    message.message_id = 1
    message.date = datetime.now(timezone.utc)
    message.chat = chat
    message.from_user = user
    message.text = '/start'
    message.answer = AsyncMock()

    state = FSMContext(
        storage=dispatcher['storage'],
        key=user_id
    )

    with patch.object(
            handlers.users,
            'insert_one',
            AsyncMock()
    ) as mock_insert:
        await handlers.start(
            message,
            state
        )
        mock_insert.assert_called_once_with({
            "_id": user_id,
            "name": user_name,
            "created_at": ANY
        })
        message.answer.assert_called_once_with(
            f"Привет, {user_name}!"
        )
