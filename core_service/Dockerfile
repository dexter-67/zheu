FROM python:3.12.3-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install uv
RUN uv pip install --system fastapi uvicorn httpx sqlalchemy asyncpg alembic pydantic-settings passlib bcrypt==4.0.1 email-validator python-jose[cryptography]

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
