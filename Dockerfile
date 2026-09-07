FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY . .

RUN ls -la /app

CMD ["uv", "run", "uvicorn", "fastapi_app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]