from fastapi import FastAPI, Depends
from routers import openai_router, test_router
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(test_router.router)
app.include_router(openai_router.router)

