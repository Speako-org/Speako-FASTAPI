import torch.nn as nn
from transformers import BertModel


class KobertSentimentClassifier(nn.Module):
    def __init__(self, num_classes=3, dropout=0.3):
        super(KobertSentimentClassifier, self).__init__()

        self.bert = BertModel.from_pretrained("monologg/kobert")

        
        self.num_hidden_layers = 4  

        
        self.dropout = nn.Dropout(dropout)
        self.layernorm = nn.LayerNorm(768)
        
        self.attention = nn.Sequential(
            nn.Linear(768, 256),  
            nn.Tanh(),
            nn.Linear(256, 1),    
            nn.Softmax(dim=1)
        )

        
        self.classifier = nn.Sequential(
            nn.Linear(768, 512),
            nn.GELU(),
            nn.LayerNorm(512),
            nn.Dropout(dropout),
            nn.Linear(512, 256),
            nn.GELU(),
            nn.LayerNorm(256),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.GELU(),
            nn.LayerNorm(128),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes)
        )

    def forward(self, input_ids, attention_mask=None):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            output_hidden_states=True
        )

        sequence_output = outputs.last_hidden_state

        cls_output = sequence_output[:, 0, :]

        cls_output = self.layernorm(cls_output)
        cls_output = self.dropout(cls_output)

        logits = self.classifier(cls_output)

        return logits


