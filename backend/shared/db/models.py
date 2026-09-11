import json
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from shared.db.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(Text, unique=True)
    address: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(100), index=True)
    city: Mapped[str | None] = mapped_column(String(100), index=True)
    rest_type: Mapped[str | None] = mapped_column(String(100))
    cuisines: Mapped[str | None] = mapped_column(Text)
    cuisine_tags: Mapped[str | None] = mapped_column(Text)
    rating: Mapped[float | None] = mapped_column(Float, index=True)
    votes: Mapped[int] = mapped_column(Integer, default=0)
    cost_for_two: Mapped[int | None] = mapped_column(Integer, index=True)
    dish_liked: Mapped[str | None] = mapped_column(Text)
    online_order: Mapped[bool] = mapped_column(Boolean, default=False)
    book_table: Mapped[bool] = mapped_column(Boolean, default=False)
    listed_in_type: Mapped[str | None] = mapped_column(String(50))
    review_snippet: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    @property
    def cuisine_tag_list(self) -> list[str]:
        if not self.cuisine_tags:
            return []
        return json.loads(self.cuisine_tags)

    def set_cuisine_tags(self, tags: list[str]) -> None:
        self.cuisine_tags = json.dumps(tags)
