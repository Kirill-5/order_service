FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY .github/workflows .

CMD ["sh", "-c", "python -c 'import fastapi_app' 2>&1 || echo IMPORT_FAILED; sleep 3600"]