from pydantic import BaseModel, Field
from typing import List, Literal

class NlpReqDTO(BaseModel) :
  transcriptionId: int
  transcriptionS3Path: str

class NlpResult(BaseModel):
  positive_ratio: float
  negative_ratio: float
  neutral_ratio: float
  negative_sentence: List[str]
  feedBack: str = Field(default="")
  
class NlpResponseDto(BaseModel):
  transcription_id: int
  data: NlpResult

