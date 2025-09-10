import logging

from services.nlpAnalysisService import analysis
from utils.spring_api import send_result_to_spring

async def sentiment_analysis(transcriptionId: int, transcriptionS3Path: str):
    try:
        result = await analysis(transcriptionId, transcriptionS3Path)
        
        if result:
            await send_result_to_spring(result)
            logging.info(f"결과값 Spring API 전송 완료 - transcriptionId: {transcriptionId}")
        else : 
            logging.error(f"감정 분석 결과가 None입니다 - transcriptionId: {transcriptionId}, S3Path: {transcriptionS3Path}")
            raise Exception(f"NLP 분석 처리 실패 - transcriptionId: {transcriptionId}")
    except Exception as e:
        logging.error(f"sentiment_analysis 처리 중 오류 발생 - transcriptionId: {transcriptionId}, 오류: {str(e)}")
        raise Exception(f"NLP 처리 실패 - transcriptionId: {transcriptionId}, 오류: {str(e)}")
 