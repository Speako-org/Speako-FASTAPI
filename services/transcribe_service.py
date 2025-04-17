import boto3
import uuid
import os 
import asyncio
import httpx

from services.s3_service import upload_text_to_s3

from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
TRANSCRIBE_OUTPUT_PREFIX = os.environ.get("TRANSCRIBE_OUTPUT_PREFIX")
RESULT_TEXT_PREFIX = os.environ.get("RESULT_TEXT_PREFIX")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

transcribe = boto3.client('transcribe', AWS_DEFAULT_REGION)

async def transcribe_audio_and_save_text(s3_audio_uri: str) -> str:
    job_name =f"transcribe-{uuid.uuid4()}"
    transcribe.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {'MediaFileUri' : s3_audio_uri},
        MediaFormat = 'wav',
        LanguageCode = 'ko-KR',
        OutputBucketName=S3_BUCKET_NAME,
        OutputKey=TRANSCRIBE_OUTPUT_PREFIX + job_name + ".json",
        Settings = {
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10
        }
    )
    
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        print(f"[{job_name}] 대기중...")
        await asyncio.sleep(10)
        
    if status == 'COMPLETED':
        transcript_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
        
        async with httpx.AsyncClient() as client:
            response = await client.get(transcript_url)
            text = response.json()['results']['transcripts'][0]['transcript']
        
        txt_key = RESULT_TEXT_PREFIX + job_name + ".txt"
        bucket = S3_BUCKET_NAME
        result_uri = upload_text_to_s3(bucket, txt_key, text)
        return result_uri
        
    else:
        raise Exception("Transcribe 실패")
