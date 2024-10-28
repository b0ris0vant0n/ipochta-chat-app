import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from auth.database import get_async_session as get_db
from users.services import save_chat_id
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()


async def send_telegram_message(chat_id: int, message: str):
    try:
        await bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
    except AiogramError as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    username = message.chat.username
    await message.reply("Привет! Я бот уведомлений. Я сообщу вам, если придут новые сообщения!")
    async for db in get_db():
        return await save_chat_id(chat_id, username, db)


dp.include_router(router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
