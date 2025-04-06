from pydantic import BaseModel, Field
from typing import List, Literal

class SentimentTag(BaseModel):
  sentence: str = Field(..., 
                        description="The original sentence being analyzed")
  sentiment_word: str = Field(..., 
                              description="The main word or phrase expressing the emotion")
  sentiment_type: Literal['기쁨', '슬픔', '놀람', '분노', '공포', '혐오', '중립']
  sentiment_score: float = Field(..., 
                                 description="Sentiment score (0: very positive, 1: very negative)")
