from fastapi import FastAPI, Depends
from routes import sentiment_analysis_by_openai_router, transcribe_router

from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(sentiment_analysis_by_openai_router.router)

app.include_router(transcribe_router.router)