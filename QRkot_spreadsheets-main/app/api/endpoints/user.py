from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

users_router = APIRouter()


users_router.include_router(

    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
