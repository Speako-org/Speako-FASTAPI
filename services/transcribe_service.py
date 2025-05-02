import boto3
import uuid
import os 
import asyncio
import httpx
import logging

from services.s3_service import upload_text_to_s3
from utils.spring_api import send_txt_url_to_spring

from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
TRANSCRIBE_OUTPUT_PREFIX = os.environ.get("TRANSCRIBE_OUTPUT_PREFIX")
RESULT_TEXT_PREFIX = os.environ.get("RESULT_TEXT_PREFIX")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

transcribe = boto3.client('transcribe', AWS_DEFAULT_REGION)

logging.basicConfig(level=logging.INFO)


async def transcribe_audio_and_save_text(transcriptionId: int, recordS3Path: str) -> str:
    s3_audio_uri = f"s3://{S3_BUCKET_NAME}/{recordS3Path}"
    
    job_name =f"transcribe-{uuid.uuid4()}"
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName = job_name,
            Media = {'MediaFileUri' : s3_audio_uri},
            MediaFormat = 'm4a',
            LanguageCode = 'ko-KR',
            OutputBucketName=S3_BUCKET_NAME,
            OutputKey=TRANSCRIBE_OUTPUT_PREFIX + job_name + ".json",
            Settings = {
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 10
            }
        )
    except Exception as e:
        logging.error(f"Transcribe 작업 시작 오류: {str(e)}")
        raise Exception(f"Transcribe 작업 시작 오류 : {str(e)}")
    
    while True:
        try:
            result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        except Exception as e:
            logging.error(f"[{job_name}] Transcribe 상태 확인 중 오류: {str(e)}")
            await asyncio.sleep(20)
            continue
        
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        
        if status in ['COMPLETED', 'FAILED']:
            break
        
        logging.info(f"[{job_name}] 대기중...")
        await asyncio.sleep(20)
        
    if status == 'COMPLETED':
        transcript_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
        
        async with httpx.AsyncClient() as client:
            try : 
                response = await client.get(transcript_url)
                text = response.json()['results']['transcripts'][0]['transcript']
                logging.info(f"[{job_name}] Transcribe 완료")
                
            except Exception as e:
                logging.error(f"[{job_name}] Transcribe 결과 가져오기 오류: {str(e)}")
                raise Exception(f"Transcribe 결과 가져오기 오류: {str(e)}")
        
        txt_key = RESULT_TEXT_PREFIX + job_name + ".txt"
        bucket = S3_BUCKET_NAME
        
        result = upload_text_to_s3(bucket, txt_key, text)
        
        if result:
            await send_txt_url_to_spring(transcriptionId, txt_key)
            logging.info(f"[{job_name}] 텍스트 파일 업로드 및 Spring API 전송 완료")

        else : 
            logging.error(f"[{job_name}] S3 업로드 실패")
            
    else:
        logging.error(f"[{job_name}] Transcribe 실패")
        raise Exception("Transcribe 실패")
