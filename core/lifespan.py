from fastapi import FastAPI
from scripts.init_db import initialize_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # FastAPI 인스턴스 기동시 필요한 작업 수행. 
    print("Starting up...")
    initialize_database()
    yield
    
    #FastAPI 인스턴스 종료시 필요한 작업 수행
    print("Shutting down...")