from pydantic import BaseModel


class PredictRequest(BaseModel):
    prompt: str


class PredictResponse(BaseModel):
    optimized_prompt: str
    total_token_usage: int