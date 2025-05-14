import os
import httpx
import logging

from dotenv import load_dotenv
from schemas.nlp_scheme import NlpResponseDto

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

async def send_result_to_spring(response: NlpResponseDto):
  post_url = os.getenv("SPRING_POST_NLP_URL")

  payload = response.model_dump()  

  try:
    async with httpx.AsyncClient() as client:
      http_response = await client.post(post_url, json=payload)
      http_response.raise_for_status()
      return http_response.json()
  except httpx.RequestError as e:
    logging.error(f"[Spring 전송 실패] 연결 문제: {e}")
    return {"error": "Spring 서버와 연결할 수 없습니다."}