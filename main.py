from fastapi import FastAPI, Depends
from router import openai_router
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(openai_router.router)

