# Бэкенд для Спортивного cайта fast-leagues

## Обзор

Этот проект — бэкенд-приложение, созданное с использованием FastAPI для спортивного сайта. 
Оно предоставляет API-эндпоинты для управления спортивными событиями, 
командами, игроками, аутентификацией пользователей и многим другим.

## Возможности

* CRUD-операции для команд, игроков и событий
* Обновление спортивных данных в реальном времени
* Аутентификация пользователей (JWT-авторизация и регистрация)
* Автоматическая документация API с openapi

## Технологии

* Бэкенд: FastAPI, SQLAlchemy, Pydantic
* База данных: PostgreSQL
* Аутентификация: JWT (JSON Web Tokens)
* Контейнеризация: Docker
* Деплой: Uvicorn/Gunicorn

## Установка

### Предварительные требования

* Python 3.12+
* Docker (опционально)

## Настройка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/sports-fastapi-backend.git
   cd sports-fastapi-backend
   ```

2. Создайте виртуальное окружение:

    ```
    python -m venv venv
    source venv/bin/activate  # Для Windows: `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```
    pip install -r requirements.txt
    ```

4. Запустите приложение:

    ```
    python src/main.py
    ```

## Документация API

После запуска сервера документация openapi будет доступна 
по адресy http://127.0.0.1:8000/docs

## Запуск с Docker

1. Соберите и запустите контейнер:

    ```
    docker-compose up --build
    ```

2. Приложение будет доступно по адресу http://localhost:5000

## Тестирование

Для запуска тестов выполните команду:

```
pytest tests/
```

