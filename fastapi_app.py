from fastapi import FastAPI

from presentation.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app