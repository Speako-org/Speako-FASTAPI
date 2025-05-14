import logging

from services.nlpAnalysisService import analysis
from utils.spring_api import send_result_to_spring

async def sentiment_analysis(transcriptionId: int):
    
    result = await analysis(transcriptionId)
    
    if result:
        await send_result_to_spring(result)
        logging.info(f"[{result}] 결과값 Spring API 전송 완료")
    else : 
        logging.error(f"결과 전송 실패")
        raise Exception("NLP 처리 실패")
 