import boto3
import os 
import httpx
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')

def upload_text_to_s3(bucket, key, text):
    try : 
        s3.put_object(Bucket=bucket, Key=key, Body = text.encode('utf-8'))
        return f"s3://{bucket}/{key}"
    except Exception as e:
        print(f"S3 업로드 오류 : {e}")
        return None
    
def convert_to_s3_uri(bucket: str, s3_path: str) ->str:
    return f"s3://{bucket}/{s3_path}"

def convert_to_url(s3_path: str) ->str:
    bucket = os.environ.get("S3_BUCKET_NAME")
    region = os.environ.get("AWS_DEFAULT_REGION")
    return f"https://{bucket}.s3.{region}.amazonaws.com/{s3_path}"

async def get_text_from_s3(s3_url: str) ->str:
    async with httpx.AsyncClient() as client:
        response = await client.get(s3_url)
        if response.status_code != 200:
            raise Exception(f"s3에서 파일을 불러오는데 실패했습니다.: {s3_url}")
        return response.text