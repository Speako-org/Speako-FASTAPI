from fastapi import APIRouter, BackgroundTasks
import asyncio

from schemas.stt_schema import TranscribeReqDTO
from services.transcribe_service import transcribe_audio_and_save_text

router = APIRouter(
    prefix = "/transcribe",
    tags = ["STT"]
)

@router.post("/start")
async def start_stt(request: TranscribeReqDTO, background_tasks: BackgroundTasks):
    try: 
        background_tasks.add_task(
            transcribe_audio_and_save_text,
            request.transcriptionId,
            request.recordS3Path
        )
        return {"message": "STT 작업이 시작되었습니다."}
    
    except Exception as e:
        return {"message" : "STT 작업 시작 중 오류가 발생했습니다", "error" : str(e)}