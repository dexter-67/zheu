# Система управления ЖЭУ

Микросервисная система для взаимодействия жителей и управляющей компании.

Проект реализован с использованием FastAPI, PostgreSQL, RabbitMQ, WebSocket и Docker Compose.

---

# Возможности

* JWT авторизация и аутентификация
* Роли пользователей (`resident`, `admin`)
* CRUD операции для новостей
* CRUD операции для заявок
* Система уведомлений
* WebSocket уведомления в реальном времени
* RabbitMQ для асинхронного взаимодействия сервисов
* API Gateway
* Docker Compose инфраструктура
* Минималистичный frontend

---

# Архитектура проекта

Проект построен на микросервисной архитектуре и состоит из следующих сервисов:

| Сервис               | Назначение                 |
| -------------------- | -------------------------- |
| core_service         | Авторизация и пользователи |
| news_service         | Новости                    |
| requests_service     | Заявки                     |
| notification_service | Уведомления                |
| api-gateway          | Единая точка входа         |
| frontend             | Клиентская часть           |
| postgres             | База данных                |
| rabbitmq             | Брокер сообщений           |

---

# Технологии

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT
* RabbitMQ

## Frontend

* HTML
* CSS
* JavaScript

## Infrastructure

* Docker
* Docker Compose
* KrakenD API Gateway

---

# Структура проекта

```text
zheu/
├── core_service/
├── news_service/
├── requests_service/
├── notification_service/
├── frontend/
├── infra/
├── docker-compose.yml
└── README.md
```

---

# Запуск проекта

## 1. Клонировать репозиторий

```bash
git clone https://github.com/dexter-67/zheu.git
cd zheu
```

---

## 2. Создать `.env`

Пример:

```env
POSTGRES_USER=zheu
POSTGRES_PASSWORD=zheu
POSTGRES_DB=zheu
JWT_SECRET=secret
```

---

## 3. Запустить контейнеры

```bash
docker compose up --build
```

---

## 4. Применить миграции

```bash
docker compose exec core_service alembic upgrade head
```

---

## 5. Открыть frontend

```text
http://localhost:5500
```

---

# API

## Auth

| Метод | Endpoint         | Описание    |
| ----- | ---------------- | ----------- |
| POST  | `/auth/register` | Регистрация |
| POST  | `/auth/login`    | Авторизация |

---

## News

| Метод  | Endpoint     |
| ------ | ------------ |
| GET    | `/news`      |
| POST   | `/news`      |
| PATCH  | `/news/{id}` |
| DELETE | `/news/{id}` |

---

## Requests

| Метод | Endpoint    |
| ----- | ----------- |
| GET   | `/requests` |
| POST  | `/requests` |

---

## Notifications

| Метод | Endpoint         |
| ----- | ---------------- |
| GET   | `/notifications` |

---

# Роли пользователей

| Роль     | Описание      |
| -------- | ------------- |
| resident | Житель        |
| admin    | Администратор |

---

# WebSocket

Сервис уведомлений поддерживает WebSocket соединения для получения уведомлений в реальном времени.

---

# RabbitMQ

RabbitMQ используется для асинхронного взаимодействия между сервисами и доставки уведомлений.
