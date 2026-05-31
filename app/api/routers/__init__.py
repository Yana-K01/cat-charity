from fastapi import APIRouter

from app.api.routers.charity_project import router as charity_project_router
from app.api.routers.donation import router as donation_router
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserRead, UserCreate, UserUpdate

main_router = APIRouter()
main_router.include_router(charity_project_router)
main_router.include_router(donation_router)

# auth/users роутеры
main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=('auth',),
)
main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=('auth',),
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

# Отключение удаления пользователей
users_router.routes = [
    route for route in users_router.routes
    if 'DELETE' not in getattr(route, 'methods', set())
]

main_router.include_router(
    users_router,
    prefix='/users',
    tags=('users',),
)
