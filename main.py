from fastapi import FastAPI, Depends
from routes import sentiment_analysis_by_openai_router
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(sentiment_analysis_by_openai_router.router)

