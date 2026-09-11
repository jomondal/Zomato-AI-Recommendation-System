from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from phase2.api.deps import get_db
from phase2.schemas.filters import FilterOptionsResponse
from phase2.services.stats_service import get_filter_options

router = APIRouter(prefix="/api/v1", tags=["filters"])


@router.get("/filters/options", response_model=FilterOptionsResponse)
def filter_options(db: Session = Depends(get_db)) -> FilterOptionsResponse:
    return FilterOptionsResponse(**get_filter_options(db))
