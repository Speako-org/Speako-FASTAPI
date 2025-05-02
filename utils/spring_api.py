import os
import httpx

from dotenv import load_dotenv

load_dotenv()

async def send_txt_url_to_spring(transcriptionId: int, transcriptionS3Path: str):
    raw_post_url= os.getenv("SPRING_POST_TRANSCRIPTION_URL")
    post_url = raw_post_url.format(transcriptionId=transcriptionId)

    params = {
        "transcriptionS3Path": transcriptionS3Path
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(post_url, params=params)
        response.raise_for_status()
        return response.json()