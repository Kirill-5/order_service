import os

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING", "").replace("postgres://", "postgresql+asyncpg://", 1)

CATALOG_SERVICE_URL = os.getenv(
    "CATALOG_SERVICE_URL",
    "http://student-system-capashino-web.student-system-capashino.svc:8000",
)
CATALOG_SERVICE_API_KEY = os.getenv("CATALOG_SERVICE_API_KEY")