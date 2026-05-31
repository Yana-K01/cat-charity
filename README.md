# QRKot — благотворительный фонд поддержки котиков (FastAPI)

REST API для управления благотворительными проектами и пожертвованиями.

Сервис умеет:
- создавать/редактировать/удалять благотворительные проекты;
- принимать пожертвования;
- автоматически распределять поступившие средства по открытым проектам.

## Стек

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- Alembic
- SQLite
- Pytest (для тестов)

## Быстрый старт

### 1) Клонирование и установка зависимостей

```bash
git clone https://github.com/Yana-K01/cat-charity
cd cat-charity-2
python -m venv venv
```

## Windows:
```bash
venv\Scripts\activate
```
## Linux/Mac:
```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 2) Переменные окружения

По умолчанию используется SQLite-файл fastapi.db в корне проекта.
А переменная берётся из настройки database_url (Pydantic Settings).

### 3) Миграции

```bash
alembic upgrade head
```

### 4) Запуск приложения

```bash
uvicorn app.main:app --reload
```

После запуска документация OpenAPI доступна по адресам:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Пользователи и авторизация

В проекте реализованы пользователи и авторизация по JWT. Типовые эндпоинты:
- POST /auth/register — регистрация пользователя
- POST /auth/jwt/login — логин (получение токена)
- GET /users/me — профиль текущего пользователя

### Регистрация:
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"string"}'
```

### Логин:
```bash
curl -X POST "http://127.0.0.1:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=string"
```

### Запрос с токеном:
```bash
curl -X POST "http://127.0.0.1:8000/donation/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"full_amount":250,"comment":"For cats"}'
  ```


## Логика инвестирования

Сервис автоматически распределяет деньги между проектами и пожертвованиями:
- При создании пожертвования свободная сумма инвестируется в самые ранние открытые проекты (по create_date, затем по id).
- При создании проекта он сразу получает инвестиции из самых ранних открытых пожертвований.
- Когда invested_amount достигает full_amount, объект помечается как fully_invested=True и получает close_date.

## API

### Благотворительные проекты

- GET /charity_project/ — список проектов (доступно без авторизации)
- POST /charity_project/ — создать проект (только суперюзер)
- PATCH /charity_project/{project_id} — изменить проект (только суперюзер)
- DELETE /charity_project/{project_id} — удалить проект (только суперюзер)
- Создание проекта (POST /charity_project/):
```bash
{
  "name": "plushcats4life",
  "description": "Huge fan of plush cats. Wanna buy a lot",
  "full_amount": 1000000
}
```

Ограничения:
- name: строка 5…100 символов, уникальна;
- description: строка от 10 символов;
- full_amount: целое положительное число;
- лишние поля в запросе запрещены.

Правила изменения/удаления:
- закрытый проект (fully_invested=True) нельзя редактировать;
- нельзя уменьшить full_amount ниже уже вложенной суммы (invested_amount);
- нельзя удалять проекты, в которые уже внесены средства (или которые закрыты).

### Пожертвования

- GET /donation/ — список пожертвований.
- POST /donation/ — создать пожертвование.

### Создание пожертвования (POST /donation/):
```bash
{
  "full_amount": 500,
  "comment": "For cats"
}
```

Ограничения:
- full_amount: целое положительное число;
- comment — необязательное поле;
- лишние поля в запросе запрещены.

## Примеры запросов

Создать проект:
```bash
curl -X POST "http://127.0.0.1:8000/charity_project/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"new_project","description":"Help homeless cats","full_amount":1000}'
```

Создать пожертвование:
```bash
curl -X POST "http://127.0.0.1:8000/donation/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"full_amount":250,"comment":"Take my money"}'
```

Посмотреть список проектов:
```bash
curl "http://127.0.0.1:8000/charity_project/"
```

## Тестирование

```bash
pytest
```

## Контакты
- GitHub: [@Yana-K01](https://github.com/Yana-K01)
- Почта: [yvk4x2@gmail.com](mailto:yvk4x2@gmail.com)
