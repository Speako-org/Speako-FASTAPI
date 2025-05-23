import random
import torch
import logging

from utils.nlpUtils import load_device, load_model, load_tokenizer
from utils.textUtils import get_text, preprocess_text
from schemas.nlp_scheme import NlpResult, NlpResponseDto
from services.s3_service import convert_to_url, get_text_from_s3


async def analysis(transcriptionId: int, transcriptionS3Path: str):
    model_path='nlp_model/3class.pt'
    
    try:
        print("감정 분석을 시작합니다.")
        
        device = load_device()
        tokenizer = load_tokenizer()
        model = load_model(model_path, device)

        s3_url = convert_to_url(transcriptionS3Path)
        raw_text = await get_text_from_s3(s3_url)
        texts = get_text(raw_text)
        
        results = {'positive': 0, 'negative': 0 ,'neutral': 0}
        most_negative_sentence = []
        
        for text in texts:
            print(text)
            predict = predict_text(text, model, tokenizer, device)
            
            print("감정 분석 결과:")
            print(f"텍스트: {text}")
            print(f"예측된 감정: {predict['sentiment']}")
            print(f"공격성 점수: {predict['aggressive_score']:.4f}")
            
            if predict['aggressive_score'] >= 0.9 and len(text) <= 20:
                most_negative_sentence.append(text)
            
            
            results[predict['sentiment']] += 1
        
        total_sentence = sum(results.values(), 0)
        positive_ratio = round(results['positive'] / total_sentence, 3)  
        negative_ratio = round(results['negative'] / total_sentence, 3)
        neutral_ratio = round(results['neutral'] / total_sentence, 3)
        
        if len(most_negative_sentence) > 2:
            negative_sentence = random.sample(most_negative_sentence, 3)
        else:
            negative_sentence = most_negative_sentence
        
        nlpResponse = NlpResult(
                positive_ratio=positive_ratio,
                negative_ratio=negative_ratio,
                neutral_ratio=neutral_ratio,
                negative_sentence=negative_sentence
            )
    except Exception as e:
        logging.error(f"감정 분석 중 오류 발생: {str(e)}")
        return 
    
    
    return NlpResponseDto(
        data=nlpResponse,
        transcriptionId=transcriptionId
    )


def predict_text(text, model, tokenizer, device):
    text = preprocess_text(text)
        
    encoding = tokenizer(
        text,
        add_special_tokens=True,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    
    model.eval()
    
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        
    probabilities = torch.softmax(logits, dim=1)
    _, predicted = torch.max(logits, 1)
    
    sentiment_classes = ['positive', 'negative', 'neutral']
    
    sentiment_idx = predicted.item()
    print(f"sentiment_idx: {sentiment_idx}")
    sentiment = sentiment_classes[sentiment_idx]
    aggressive_score = probabilities[0][1].item()
    
    return {
        'sentiment': sentiment,
        'aggressive_score': aggressive_score
    }