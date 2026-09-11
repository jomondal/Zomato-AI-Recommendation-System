from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    city: str | None = None
    location: str | None = None
    min_rating: float | None = Field(None, ge=0, le=5)
    max_rating: float | None = Field(None, ge=0, le=5)
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)
    cuisines: list[str] = Field(default_factory=list)
    free_text: str | None = None
    use_llm: bool = True
    limit: int = Field(default=10, ge=1, le=50)


class RecommendationItem(BaseModel):
    rank: int
    restaurant_id: int
    name: str
    rating: float | None
    votes: int
    cost_for_two: int | None
    location: str | None
    city: str | None
    cuisines: str | None
    match_score: int
    reason: str
    highlights: list[str]
    url: str | None
    online_order: bool
    book_table: bool


class RecommendResponse(BaseModel):
    summary: str
    total_candidates: int
    recommendations: list[RecommendationItem]
    latency_ms: int
    source: str = "rule_based"
    llm_latency_ms: int | None = None
