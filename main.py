from fastapi import FastAPI, Depends

from routes import test_router, transcribe_router

from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(test_router.router)

app.include_router(transcribe_router.router)