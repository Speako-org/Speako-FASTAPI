import re
from langchain_community.document_loaders import TextLoader

def get_text(raw_text: str)-> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', raw_text.strip())

    filtered_docs = [s.strip() for s in sentences if s.strip()]
    
    return filtered_docs 

def preprocess_text(text):
    text = re.sub(r'[^\w\s\.\,\!\?]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text