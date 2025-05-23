import re
from langchain_community.document_loaders import TextLoader

def get_text(raw_text: str)-> list[str]:
    lines = raw_text.strip().split("\n")

    # 공백을 제거한 뒤 문자가 남는다면 list에 추가함
    filtered_docs = [line.strip() for line in lines if line.strip()]
    
    return filtered_docs  # 처음 10줄만 반환

def preprocess_text(text):
    text = re.sub(r'[^\w\s\.\,\!\?]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text