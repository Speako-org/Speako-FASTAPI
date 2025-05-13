# routers/test_router.py

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.nlp_response_service import sentiment_analysis

router = APIRouter()

@router.post("/analysis")
async def run_test_analysis():
  await sentiment_analysis()
  return JSONResponse(
    status_code=status.HTTP_200_OK
  )