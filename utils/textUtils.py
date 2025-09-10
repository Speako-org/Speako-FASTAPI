import re
import json
from langchain_community.document_loaders import TextLoader

def get_text(raw_text: str)-> list[str]:
    # 빈 텍스트 처리
    if not raw_text or not raw_text.strip():
        return []
    
    sentences = re.split(r'(?<=[.!?])\s+', raw_text.strip())

    filtered_docs = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 1]
    
    return filtered_docs 

def preprocess_text(text):
    text = re.sub(r'[^\w\s\.\,\!\?]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


async def get_speaker_text_only(raw_json: str, target_speaker="spk_0"):
    data = json.loads(raw_json)
    results = data.get("results", {})
    segments = results.get("audio_segments", [])

    texts = []
    
    for seg in segments:
        if seg.get("speaker_label") == target_speaker:
            transcript = seg.get("transcript", "").strip()
            if transcript:
                texts.append(transcript)
                
    return " ".join(texts)