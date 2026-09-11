from pydantic import BaseModel, Field


class LlmRecommendationItem(BaseModel):
    restaurant_id: int
    rank: int = Field(ge=1)
    match_score: int = Field(ge=0, le=100)
    reason: str
    highlights: list[str] = Field(default_factory=list)
    best_for: str | None = None


class LlmRecommendResponse(BaseModel):
    summary: str
    recommendations: list[LlmRecommendationItem]
