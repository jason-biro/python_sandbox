import pytest
import httpx
from fastapi import FastAPI
from sqlalchemy import select
from models import NHLTeamStat

from httpx import ASGITransport

# Set the default backend driver configuration for pytest
pytestmark = pytest.mark.anyio

@pytest.fixture
async def client(test_app: FastAPI) -> httpx.AsyncClient:
    """Provides an asynchronous client container for standard route testing."""
    transport = ASGITransport(app=test_app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def test_trigger_ingestion_endpoint_handshake(client: httpx.AsyncClient):
    """Verifies that the ingestion endpoint registers and confirms jobs successfully."""
    response = await client.post("/api/v1/scraper/ingest?pages=2")

    assert response.status_code == 202
    json_data = response.json()
    assert json_data["status"] == "Accepted"
    assert json_data["targetPages"] == 2

async def test_get_teams_endpoint_returns_data(client: httpx.AsyncClient, db_session):
    """Ensures data seeded in the database is correctly serialized and returned by the API."""
    # Seed mock data into the isolated test database.
    async with db_session.begin():
        mock_team = NHLTeamStat(
            team_name="Test Team",
            year=2023,
            wins=10,
            losses=5,
            win_percentage=0.667
        )
        db_session.add(mock_team)

    # Query the endpoint using the test client
    response = await client.get("/api/v1/teams?year=2023&limit=5")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["teamName"] == "Test Team"
    assert data[0]["year"] == 2023
