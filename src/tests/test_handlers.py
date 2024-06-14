import pytest
from unittest.mock import AsyncMock, MagicMock, patch, ANY
from aiogram.types import Message, User, Chat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from src.bot.handlers import BotHandlers
from src.config.base import settings
from src.db import get_db_collections
from aiogram import Bot, Dispatcher
from datetime import datetime, timezone



@pytest.fixture
def bot():
    return Bot(token=settings.TOKEN)


@pytest.fixture
def dispatcher(bot):
    return Dispatcher(storage=MemoryStorage())


@pytest.fixture
def db_collections():
    return get_db_collections()


@pytest.fixture
def handlers(bot):
    return BotHandlers(bot)


@pytest.mark.asyncio
async def test_start_handler(handlers):
    user_id = 123
    user_name = "TestUser"
    user = User(id=user_id, is_bot=False, first_name=user_name)
    chat = Chat(id=user_id, type="private")
    message = Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text='/start'
    )
    message.answer = AsyncMock()

    state = FSMContext(
        storage=MemoryStorage(), user=message.from_user, chat=message.chat
    )

    with patch.object(handlers.users, 'insert_one', AsyncMock()) as mock_insert:
        await handlers.start(message, state)
        mock_insert.assert_called_once_with({
            "_id": user_id,
            "name": user_name,
            "created_at": ANY
        })
        message.answer.assert_called_once_with(f"Привет, {user_name}!")


