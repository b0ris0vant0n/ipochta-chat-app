import json
from datetime import datetime

from fastapi import WebSocketDisconnect, Depends, APIRouter
from fastapi_users import BaseUserManager

from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session as get_db
from messaging.schemas import MessageCreate

from auth.database import User
from messaging.services import send_message
from users.services import get_user_by_username
from celery_app import send_telegram_notification
from fastapi import WebSocket, HTTPException
from fastapi_users.authentication import JWTStrategy
from config import SECRET
from auth.manager import get_user_manager

jwt_strategy = JWTStrategy(secret=SECRET, lifetime_seconds=3600)

router = APIRouter()

connected_clients = {}


@router.websocket("/ws/{username}")
async def websocket_endpoint(
        websocket: WebSocket,
        username: str,
        db: AsyncSession = Depends(get_db),
        user_manager: BaseUserManager[User, int] = Depends(get_user_manager)
):
    token = websocket.cookies.get("messaging")
    if not token:
        raise HTTPException(status_code=403, detail="JWT token not found in cookies")
    try:
        user = await jwt_strategy.read_token(token, user_manager)
        print(f'user - {user.username}')
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid JWT token")

    if not user:
        raise HTTPException(status_code=403, detail="Invalid JWT token")

    await websocket.accept()

    connected_clients[user.username] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_json = json.loads(data)
                recipient_username = username
                content = message_json["content"]
            except (json.JSONDecodeError, KeyError):
                await websocket.send_text(
                    "Invalid message format. Expected JSON with 'recipient' and 'content' fields.")
                continue

            recipient = await get_user_by_username(recipient_username, db)

            if recipient and user:
                message_data = MessageCreate(
                    sender_id=user.id,
                    recipient_id=recipient.id,
                    content=content
                )
                await send_message(message_data, db)

                if recipient_username in connected_clients:
                    recipient_ws = connected_clients[recipient_username]
                    await recipient_ws.send_text(json.dumps({
                        "sender": user.username,
                        "content": content,
                        "timestamp": datetime.utcnow().isoformat()
                    }))
                else:
                    send_telegram_notification.delay(recipient.telegram_chatid, content, user.username)
            else:
                await websocket.send_text("Recipient not found.")

    except WebSocketDisconnect:
        connected_clients.pop(user.username, None)
        await websocket.close()
