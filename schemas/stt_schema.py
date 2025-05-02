from pydantic import BaseModel

class TranscribeReqDTO(BaseModel) :
    transcriptionId: int
    recordS3Path: str
