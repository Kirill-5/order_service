FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync

COPY .github/workflows .

CMD ["sh", "-c", "ls -la /app && sleep 3600"]