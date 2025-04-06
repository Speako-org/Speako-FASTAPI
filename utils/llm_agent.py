from dotenv import load_dotenv
from os import getenv
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API = getenv("OPENAI_API_KEY")

def get_llm(model='gpt-4o'):
    return ChatOpenAI(
        temperature=0,
        model=model,
        request_timeout=120,
        max_tokens=4000
    )
    

# 구조화된 출력을 위한 LLM 인스턴스 반환
def get_structured_llm(model_class):
    llm = get_llm()
    return llm.with_structured_output(model_class)
