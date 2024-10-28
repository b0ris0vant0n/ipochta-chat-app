from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from messaging.routes import router as messaging_route
from messaging.websockets import router as websockets_route
from users.routes import router as user_routes

app = FastAPI(
    title="Messaging App"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_user = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authorization"],
)

app.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authorization"],
)

current_user = fastapi_user.current_user()


app.include_router(messaging_route)
app.include_router(websockets_route)
app.include_router(user_routes)
