from utils import llm_agent
from schemas.sentiment_schema import SentimentTag
from typing import List

# txt 파일을 읽기 위한 것
from langchain_community.document_loaders import TextLoader

# 테스트용 운수 좋은날 텍스트
def get_sentence(file_path="TestData/운수좋은날.txt"):
    loader = TextLoader(file_path)
    docs = loader.load()
    
    lines = docs[0].page_content.split("\n")

    # 공백을 제거한 뒤 문자가 남는다면 list에 추가함
    filtered_docs = [line.strip() for line in lines if line.strip()]
    
    return filtered_docs[:10]  # 처음 10줄만 반환

#토큰 수에 제한이 있기 때문에 한 문장 씩 분석, 나중에 변경 가능
def analyze_single_sentence(sentence, structured_llm):

    prompt = f"""
    다음 문장에 대해 감정 분석을 해주세요.

    출력 형식:
    - sentence: 입력 문장 그대로
    - sentiment_word: 문장에서 가장 감정을 잘 드러내는 단어나 구
    - sentiment_type: 문장을 대표하는 감정 한 가지 (기쁨, 슬픔, 놀람, 분노, 공포, 혐오, 중립 중에서 선택)
    - sentiment_score: 감정 강도를 0~1 사이의 숫자로 표현 (0은 매우 긍정적, 1은 매우 부정적, 0.5는 중립)

    문장: "{sentence}"
    """
    
    try:
        response = structured_llm.invoke(prompt)
        return response  # ✅ 이제 response는 SentimentTag 하나!
    except Exception as e:
        print(f"문장 분석 중 오류 발생: {str(e)}")
        return None


def analyzs_sentiment(sentences: List[str] = None):
    # 문장이 제공되지 않으면 기본 문장 가져오기
    if sentences is None:
        sentences = get_sentence()
    
    # LLM 모델 초기화
    structured_llm = llm_agent.get_structured_llm(SentimentTag)
    
    all_results = []
    
    # 각 문장을 개별적으로 분석
    for sentence in sentences:
        print(f"[분석 중] {sentence}")
        result = analyze_single_sentence(sentence, structured_llm)
        if result:
            all_results.append(result)
        else:
            print(f"[실패] {sentence}")
    
    # Pydantic 모델을 dict로 변환
    data = [tag.model_dump() for tag in all_results]
    
    print(data)
    return data