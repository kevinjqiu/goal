from sqlalchemy import Column, ForeignKey, Integer, func, or_
from sqlalchemy.orm import relationship
from .base import Base
from .fixture import Fixture
from .team_season import TeamSeason


class Season(Base):
    __tablename__ = 'season'
    season_id = Column(Integer, primary_key=True)
    competition_id = Column(
        Integer, ForeignKey('competition.competition_id'), nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)

    teams = relationship('Team', secondary=TeamSeason.__table__)

    def __json__(self):
        return {
            'id': self.season_id,
            'competition_id': self.competition_id,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'num_game_days': self.get_num_of_gamedays(self.season_id),
            'next_game_day': self.get_next_game_day(self.season_id),
        }

    def __repr__(self):
        return "<Season: {}>".format(self.season_id)

    @classmethod
    def get_by_id(cls, season_id):
        return cls.session.query(Season).filter_by(season_id=season_id).one()

    @classmethod
    def get_num_of_gamedays(cls, season_id):
        return (
            cls.session.query(func.max(Fixture.game_day))
            .filter(Fixture.season_id == season_id)
            .scalar())

    @classmethod
    def get_next_game_day(cls, season_id):
        query = (
            cls.session.query(func.min(Fixture.game_day))
            .filter(or_(
                Fixture.home_score == None,  # noqa
                Fixture.away_score == None))
            .filter(Fixture.season_id == season_id)
        )
        return query.scalar()
