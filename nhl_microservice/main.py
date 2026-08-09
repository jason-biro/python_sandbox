from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, BackgroundTasks
from sqlalchemy import select

from database import engine, Base, AsyncSessionLocal
from models import NHLTeamStat
import schemas
import scraper

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown tasks.
    Replaces the deprecated on_event structure.
    """
    print("[*] LifeCycle: Initializing database architecture maps...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield # The API runs its full server session while paused on this yield statement.

    print("[*] LifeCycle: Cleaning up microservice resources...")
    # Add any explicit database pool disconnects here if needed in production.

app = FastAPI(
    title="NHL Async Analytics Pipeline",
    description="Decoupled Microservice with Managed Native Background Processing Queues.",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/api/v1/scraper/ingest", response_model=schemas.IngestionTriggerResponse, status_code=202)
async def trigger_ingestion(
    background_tasks: BackgroundTasks,
    pages: int = Query(default=3, ge=1, le=10)
):
    """
    Registers a target scraper workload onto the async processing queue,
    instantly returning an acknowledgement back to the caller.
    """
    # Enqueue work to the background task executor framework.
    background_tasks.add_task(scraper.run_background_ingestion, pages)

    return {
        "status": "Accepted",
        "message": "Scraper tracking task successfully assigned to processing queue.",
        "target_pages": pages
    }

@app.get("/api/v1/teams", response_model=List[schemas.TeamStatResponse])
async def get_team_stats(
    year: Optional[int] = Query(None, description="Filter results by target production year parameters."),
    limit: int = Query(default=20, ge=1, le=100)
):
    """Fetches paginated results safely using a standard database context pipeline layout."""
    async with AsyncSessionLocal() as session:
        query = select(NHLTeamStat)

        if year:
            query = query.where(NHLTeamStat.year == year)

        query = query.limit(limit)
        db_execution_result = await session.execute(query)
        records = db_execution_result.scalars().all()

        return records
