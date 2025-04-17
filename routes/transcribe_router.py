from fastapi import APIRouter
import asyncio

from services.db_service import get_pending_audio_path
from services.s3_service import upload_text_to_s3, convert_to_s3_uri
from services.transcribe_service import transcribe_audio_and_save_text
#from utils.spring_api import send_txt_url_to_spring

router = APIRouter(
    prefix = "/stt",
    tags = ["STT"]
)

@router.post("/run-all")
async def transcribe_audio():
    records = get_pending_audio_path()
    
    async def process_record(record):
        try:
            s3_uri = convert_to_s3_uri(record['s3_path'])
            print(s3_uri)
            txt_url = await transcribe_audio_and_save_text(s3_uri)
            
            return {
                "record_id" : record['record_id'],
                "status": "success",
                "txt_url": txt_url
                
            }
        except Exception as e:
            return {
                "record_id" : record['record_id'],
                "status": "fail",
                "error" : str(e)
            }
            
    tasks = [process_record(record) for record in records]
    results = await asyncio.gather(*tasks)
    
    return {"results": results}