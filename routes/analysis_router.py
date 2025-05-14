# routers/test_router.py

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from services.nlp_response_service import sentiment_analysis
from schemas.nlp_scheme import NlpReqDTO

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/start")
async def run_test_analysis(request: NlpReqDTO):
  await sentiment_analysis(request.transcriptionId)
  return JSONResponse(
    status_code=status.HTTP_200_OK
  )