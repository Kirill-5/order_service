FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY . .

ENV PYTHONPATH=/app

CMD ["sh", "-c", "python bin/run.py 2>&1 || echo RUN_FAILED; sleep 3600"]