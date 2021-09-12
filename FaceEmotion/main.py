from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from .models import manage
from .routers import rekognition

app = FastAPI(
    title="Face Emotion",
    description="Face Emotion Description",
    version="0.0.1",
)

app.mount("/static", StaticFiles(directory="FaceEmotion/static"), name="static")

manage.create_all()

app.include_router(rekognition.router)
