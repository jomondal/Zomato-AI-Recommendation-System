from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from phase2.api.routes import filters, health, recommend, restaurants, stats
from phase5.app_setup import configure_production_app
from shared.config import settings
from shared.db.database import init_db

app = FastAPI(
    title="Zomato AI Recommendation API",
    description="Phase 5 — Production-ready Groq recommendations with Redis cache and observability",
    version="0.5.0",
)

configure_production_app(app)

origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(recommend.router)
app.include_router(restaurants.router)
app.include_router(stats.router)
app.include_router(filters.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Zomato AI Recommendation API", "docs": "/docs"}
