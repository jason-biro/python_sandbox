from pydantic import BaseModel, Field, ConfigDict

class TeamStatResponse(BaseModel):
    """Validates outwards facing payload structure."""
    id: int
    team_name: str = Field(..., serialization_alias="teamName", description="The name of the team")
    year: int
    wins: int
    losses: int
    win_percentage: float = Field(..., serialization_alias="winPercentage", description="The win percentage of the team")

    model_config = ConfigDict(from_attributes=True)

class IngestionTriggerResponse(BaseModel):
    """Immediate client handshake data schema."""
    status: str
    message: str
    target_pages: int = Field(..., serialization_alias="targetPages", description="The number of pages targeted for ingestion")
