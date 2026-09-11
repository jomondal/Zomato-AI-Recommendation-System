from pydantic import BaseModel, Field


class RestaurantOut(BaseModel):
    id: int
    name: str
    url: str | None
    address: str | None
    location: str | None
    city: str | None
    rest_type: str | None
    cuisines: str | None
    cuisine_tags: list[str]
    rating: float | None
    votes: int
    cost_for_two: int | None
    dish_liked: str | None
    online_order: bool
    book_table: bool
    listed_in_type: str | None
    review_snippet: str | None

    model_config = {"from_attributes": True}


class RestaurantListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[RestaurantOut]


class RestaurantFilters(BaseModel):
    city: str | None = None
    location: str | None = None
    min_rating: float | None = Field(None, ge=0, le=5)
    max_rating: float | None = Field(None, ge=0, le=5)
    min_price: int | None = Field(None, ge=0)
    max_price: int | None = Field(None, ge=0)
    cuisines: list[str] = Field(default_factory=list)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
