import boto3
from datetime import datetime 
from urllib.parse import urlparse, unquote

s3 = boto3.client('s3')

def upload_text_to_s3(bucket, key, text):
    try : 
        s3.put_object(Bucket=bucket, Key=key, Body = text.encode('utf-8'))
        return f"s3://{bucket}/{key}"
    except Exception as e:
        print(f"S3 업로드 오류 : {e}")
        return None
    
def convert_to_s3_uri(http_url):
    parsed_url = urlparse(http_url)
    bucket = parsed_url.netloc.split('.')[0]
    
    key = unquote(parsed_url.path.lstrip('/')).replace('+', ' ')
    return f"s3://{bucket}/{key}"