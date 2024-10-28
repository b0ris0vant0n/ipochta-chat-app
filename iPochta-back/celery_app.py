from celery import Celery
import asyncio
from telegram_bot import send_telegram_message
import logging
from config import BROKER_URL, RESULT_BACKEND

celery_app = Celery("tasks", broker=BROKER_URL, backend=RESULT_BACKEND)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task
def send_telegram_notification(chat_id: int, message_content: str, username: str):
    if chat_id:
        message = f"У вас новое сообщение от {username}: {message_content}"
        try:
            asyncio.run(send_telegram_message(chat_id, message))
            logger.info(f'Сообщение успешно отправлено {chat_id}.')
        except Exception as e:
            logger.error(f"Ошибка при выполнении задачи: {e}")
