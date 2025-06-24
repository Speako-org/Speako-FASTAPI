from utils import llm_agent
from utils.textUtils import get_text
from services.s3_service import convert_to_url, get_text_from_s3
from schemas.sentiment_schema import feedBackDto
from schemas.nlp_scheme import NlpResult

async def feedback_analysis(nlpResult: NlpResult, transcriptionId: int, transcriptionS3Path: str):
    s3_url = convert_to_url(transcriptionS3Path)
    raw_text = await get_text_from_s3(s3_url)
    texts = get_text(raw_text)
    
    full_sentence = ""
    found_negative_sentence = ""
    
    for text in texts:
        full_sentence += text
    
    for sentence in nlpResult.negative_sentence:
        found_negative_sentence += sentence
    
    prompt = f"""
    다음에 주어지는 것들은 대화의 원본 문장과 발견된 부정적 문장입니다.
    원본 문장: "{full_sentence}"
    발견된 부정적 문장: "{found_negative_sentence}"
    피드백 작성: 원본 문장에서 발견된 부정적 문장을 참고하여 피드백을 작성해주세요.
    피드백 작성 예시:
    - ~한 상황에서 ~한 문장을 사용하였는데, 이 문장을 ~ 바꾼다면 더 좋을 것 같아요.
    """
    
    # LLM 모델 초기화
    structured_llm = llm_agent.get_structured_llm(feedBackDto)
    
    try:
        response = structured_llm.invoke(prompt)
        return response  
    except Exception as e:
        print(f"피드백 생성중 오류 발생: {str(e)}")
        return None
