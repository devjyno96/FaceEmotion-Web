from fastapi import FastAPI

from .models import manage
from .routers import control

app = FastAPI(
    title="Face Emotion",
    description="Face Emotion Description",
    version="0.0.1",
)

manage.create_all()

app.include_router(log.router)