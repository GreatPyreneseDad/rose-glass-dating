"""
Pydantic Models for Analysis
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DimensionReading(BaseModel):
    """Individual dimension analysis"""
    value: float = Field(..., ge=0.0, le=1.0, description="Dimension reading 0.0-1.0")
    translation: str = Field(..., description="Human-readable translation")


class AnalysisRequest(BaseModel):
    """Request for profile analysis"""
    user_context: Optional[str] = Field(None, description="User's context/situation")
    use_premium: bool = Field(False, description="Use premium Claude model")


class UsageMetrics(BaseModel):
    """Usage and cost metrics"""
    input_tokens: int
    output_tokens: int
    cost_usd: float
    charge_usd: float
    model_used: str


class AnalysisResponse(BaseModel):
    """Analysis result response"""
    success: bool
    analysis: str
    usage: UsageMetrics
    remaining_credits: float
    analysis_id: Optional[str] = None


class AnalysisHistoryItem(BaseModel):
    """Single analysis history entry"""
    id: str
    analysis_text: str
    created_at: datetime
    model_used: str
    cost_usd: float
    charge_usd: float


class UserCredits(BaseModel):
    """User credit balance"""
    user_id: str
    credits: float
    last_updated: datetime
