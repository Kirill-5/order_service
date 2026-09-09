FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY . .

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "bin/run.py"]