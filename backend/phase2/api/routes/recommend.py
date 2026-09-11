from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from phase2.api.deps import get_db
from phase2.schemas.recommendation import RecommendRequest, RecommendResponse
from phase3.services.recommend_service import recommend_with_groq

router = APIRouter(prefix="/api/v1", tags=["recommend"])


@router.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest, db: Session = Depends(get_db)) -> RecommendResponse:
    return recommend_with_groq(db, request)
