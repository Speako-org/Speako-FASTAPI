# routers/test_router.py

from fastapi import APIRouter
from services.nlp_response_service import sentiment_analysis

router = APIRouter()

@router.post("/test-analysis")
async def run_test_analysis():
  await sentiment_analysis()
  return {"status": "sent"}