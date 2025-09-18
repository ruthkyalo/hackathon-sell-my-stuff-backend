from pydantic import BaseModel
from typing import Optional


class AnalyzeImageRequest(BaseModel):
    image: str  # Base64 encoded image


class AnalyzeImageResponse(BaseModel):
    success: bool
    message: str
    description: Optional[str] = None
    suggested_price: Optional[str] = None
