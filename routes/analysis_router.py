# routes/analysis_router.py

from fastapi import APIRouter, status, BackgroundTasks, Header, HTTPException
from fastapi.responses import JSONResponse
from services.nlp_response_service import sentiment_analysis
from schemas.nlp_scheme import NlpReqDTO
import os

router = APIRouter(prefix="/analyze", tags=["analyze"])

INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

@router.post("/start")
async def run_test_analysis(
  request: NlpReqDTO, 
  background_tasks: BackgroundTasks,
  authorization: str = Header(None)
):
  if authorization != f"Bearer {INTERNAL_SECRET}":
    raise HTTPException(status_code=401, detail="Unauthorized")
      
  try:
    background_tasks.add_task(
      sentiment_analysis,
      request.transcriptionId,
      request.transcriptionS3Path
    )
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content = {"message": "NLP 분석이 성공적으로 시작되었습니다."}
    )
    
  except Exception as e :
    return JSONResponse(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      content = {"message": "NLP 분석 작업 시작 중 오류가 발생했습니다."}
    )