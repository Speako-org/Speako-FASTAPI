import random
import torch
import logging
import heapq 

from utils.nlpUtils import load_device, load_model, load_tokenizer
from utils.textUtils import get_text, preprocess_text
from schemas.nlp_scheme import NlpResult, NlpResponseDto
from services.s3_service import convert_to_url, get_text_from_s3
from services.sentiment_feedback import feedback_analysis

logging.basicConfig(
    level=logging.INFO, 
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def analysis(transcriptionId: int, transcriptionS3Path: str):
    model_path='nlp_model/3class.pt'
    
    try:
        logging.info("감정 분석을 시작합니다.")
        
        device = load_device()
        tokenizer = load_tokenizer()
        model = load_model(model_path, device)

        s3_url = convert_to_url(transcriptionS3Path)
        raw_text = await get_text_from_s3(s3_url)
        texts = get_text(raw_text)
        
        results = {'positive': 0, 'negative': 0 ,'neutral': 0}
        most_negative_sentence = []
        
        for text in texts:
            predict = predict_text(text, model, tokenizer, device)
            
            logging.info(
                f"[감정 분석 결과] 텍스트: {text} | "
                f"예측: {predict['sentiment']} | "
                f"공격성 점수: {predict['aggressive_score']:.4f}"
            )
            
            results[predict['sentiment']] += 1
            
            score = predict['aggressive_score']
            
            if score >= 0.65 and predict['sentiment'] == 'negative':
                if len(most_negative_sentence) < 3:
                    heapq.heappush(most_negative_sentence, (score, text))
                else:
                    heapq.heappushpop(most_negative_sentence, (score, text))
            
        total_sentence = sum(results.values(), 0)
        positive_ratio = round(results['positive'] / total_sentence, 3)
        negative_ratio = round(results['negative'] / total_sentence, 3)
        neutral_ratio = round(results['neutral'] / total_sentence, 3)
        
        negative_sentence = [text for _, text in sorted(most_negative_sentence, reverse=True)]
        
        # 초기 NlpResult 생성 (피드백 없이)
        temp_nlp_result = NlpResult(
            positive_ratio=positive_ratio,
            negative_ratio=negative_ratio,
            neutral_ratio=neutral_ratio,
            negative_sentence=negative_sentence
        )
        
        # GPT 피드백 분석 수행
        logging.info("GPT 피드백 분석을 시작합니다.")
        feedback_result = await feedback_analysis(temp_nlp_result, transcriptionId, transcriptionS3Path)
        
        feedback_list = []
        
        if feedback_result and hasattr(feedback_result, 'feedBack'):
            feedback_list = [f.strip() for f in feedback_result.feedBack.split("- ") if f.strip()]
            logging.info(f"GPT 피드백 분석 완료: {feedback_list}")
        else:
            logging.warning("GPT 피드백 분석 실패 - 빈 피드백으로 진행")
        
        # 최종 NlpResult 생성 (피드백 포함)
        nlpResponse = NlpResult(
            positive_ratio=positive_ratio,
            negative_ratio=negative_ratio,
            neutral_ratio=neutral_ratio,
            negative_sentence=negative_sentence,
            feedBack=feedback_list
        )
    except Exception as e:
        logging.error(f"감정 분석 중 오류 발생: {str(e)}")
        return 
    
    
    return NlpResponseDto(
        data=nlpResponse,
        transcription_id=transcriptionId
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
    logging.debug(f"sentiment_idx: {sentiment_idx}")
    sentiment = sentiment_classes[sentiment_idx]
    aggressive_score = probabilities[0][1].item()
    
    return {
        'sentiment': sentiment,
        'aggressive_score': aggressive_score
    }