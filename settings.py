import os

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING", "").replace("postgres://", "postgresql+asyncpg://", 1)

CATALOG_SERVICE_URL = os.getenv(
    "CATALOG_SERVICE_URL",
    "http://student-system-capashino-web.student-system-capashino.svc:8000",
)
CATALOG_SERVICE_API_KEY = os.getenv("CATALOG_SERVICE_API_KEY")
PAYMENTS_SERVICE_URL = os.getenv(
    "PAYMENTS_SERVICE_URL",
    "http://student-system-capashino-web.student-system-capashino.svc:8000",
)
PAYMENTS_SERVICE_API_KEY = os.getenv("PAYMENTS_SERVICE_API_KEY")
ORDER_SERVICE_CALLBACK_URL = os.getenv(
    "ORDER_SERVICE_CALLBACK_URL",
    "http://student-kirill-5-order-service-web.student-kirill-5-order-service.svc:8000/api/orders/payment-callback",
)