from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class NHLTeamStat(Base):
    __tablename__ = "nhl_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    wins: Mapped[int] = mapped_column(Integer)
    losses: Mapped[int] = mapped_column(Integer)
    win_percentage: Mapped[float] = mapped_column(Float)
