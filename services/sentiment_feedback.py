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
    
    found_negative_sentence = nlpResult.negative_sentence
    
    prompt = f"""
    너는 심리학적 언어습관 개선을 돕는 전문가야.
    다음에 주어지는 것들은 대화의 원본 문장과 발견된 부정적 문장이야 
    원본 문장: "{full_sentence}"
    발견된 부정적 문장: "{found_negative_sentence}"
    각 리스트 항목은 하나의 부정적인 문장으로 취급하며, 아래 조건을 모두 만족하는 대체 가능한 개선안을 1:1로 제시해줘.

    조건: 
    1. 각 개선안 문장은 반드시 발견된 부정적 문장 순서와 동일하게 1:1 대응으로 작성할 것.
    2. 조건 외의 어떠한 추가 텍스트, 서론, 불필요한 설명, 큰따옴표, 리스트 기호 사용 금지.
    3. 각 개선안은 반드시 '- '로 시작하고, 각 문장은 줄바꿈(엔터)으로 구분할 것.
    4. 각 개선안은 원문 길이와 비슷하게 하되, 원문 대비 ±20자 범위 안에서 작성할 것.
    5. 개선안은 단순히 공손하거나 무턱대고 긍정적인 표현이 아니라, 자연스럽게 말할 수 있는 구어체이면서도 자기 효능감(self-efficacy)과 회복탄력성(resilience)을 키울 수 있는 긍정적 마인드셋을 담을 것.
    6. 어떤 경우에도 발견된 부정적 문장을 누락하지 말고 반드시 발견된 부정적 문장이 있는 문장 수와 동일하게 개선안 출력할 것. 
    7. 출력은 반드시 개선안만을 작성하고, 원문이나 "→"를 포함하지 말 것

    """
    
    # LLM 모델 초기화
    structured_llm = llm_agent.get_structured_llm(feedBackDto)
    
    try:
        response = structured_llm.invoke(prompt)
        return response  
    except Exception as e:
        print(f"피드백 생성중 오류 발생: {str(e)}")
        return None
