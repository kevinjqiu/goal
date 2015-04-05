from sqlalchemy import Column, String, ForeignKey, Integer
from .base import Base


class TeamSeason(Base):
    __tablename__ = 'team_season'
    team_id = Column(
        String(6), ForeignKey('team.team_id'), primary_key=True)
    season_id = Column(
        Integer, ForeignKey('season.season_id'), primary_key=True)
