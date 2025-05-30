from transformers import AutoTokenizer
import torch
from nlp_model.kobert import KobertSentimentClassifier


def load_device(): 
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    return device


def load_tokenizer():
    try:
        tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)
        print("Tokenizer 로드 성공")
        return tokenizer
    except Exception as e:
        print(f"Tokenizer 로드 실패: {e}")
        return None


def load_model(model_path, device):
    try:
        model = load_kobert_model(model_path, device)
        
        if model is None:
            print("모델 로드 실패")
            return None
        
        model.to(device)
        return model
    
    except Exception as e:
        print(f"모델 로드 중 오류 발생: {e}")
        return None


def load_kobert_model(model_path, device, dropout=0.3, num_classes=3):
    try:
        model = KobertSentimentClassifier(num_classes=num_classes, dropout=dropout)
        if model_path:
            model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device)
        return model
    except Exception as e:
        print(f"모델 로드 중 오류 발생 {e}")
        return None