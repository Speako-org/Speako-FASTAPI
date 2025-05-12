from pydantic import BaseModel, Field
from typing import List, Literal

class NlpResponse(BaseModel):
  positive_ratio: float
  negative_ratio: float
  neutral_ratio: float
  negative_sentence: List[str]
