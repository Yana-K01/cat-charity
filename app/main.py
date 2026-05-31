from fastapi import FastAPI

from app.api.routers import main_router

tags_metadata = (
    {
        'name': 'charity_projects',
        'description': 'Операции с благотворительными проектами.',
    },
    {
        'name': 'donations',
        'description': 'Операции с пожертвованиями.',
    },
    {
        'name': 'auth',
        'description': 'Аутентификация и регистрация пользователей.',
    },
    {
        'name': 'users',
        'description': 'Операции с пользователями.',
    },
)

app = FastAPI(
    title='Благотворительный фонд поддержки котиков QRKot',
    description='Сервис для поддержки котиков',
    version='0.1.0',
    openapi_tags=tags_metadata,
)

app.include_router(main_router)
