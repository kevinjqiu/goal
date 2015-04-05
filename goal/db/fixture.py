from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Fixture(Base):
    __tablename__ = 'fixture'
    fixture_id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey('season.season_id'), nullable=False)
    game_day = Column(Integer, nullable=False)
    home_team_id = Column(
        String(6), ForeignKey('team.team_id'), nullable=False)
    home_score = Column(Integer)
    away_team_id = Column(
        String(6), ForeignKey('team.team_id'), nullable=False)
    away_score = Column(Integer)

    season = relationship('Season', uselist=False, backref='fixtures')
    home_team = relationship('Team', foreign_keys=home_team_id)
    away_team = relationship('Team', foreign_keys=away_team_id)

    def __json__(self):
        return {
            'id': self.fixture_id,
            'season_id': self.season_id,
            'game_day': self.game_day,
            'home_team': self.home_team_id,
            'away_team': self.away_team_id,
            'home_score': self.home_score,
            'away_score': self.away_score,
        }

    def __repr__(self):
        return "<Fixture: {},{} vs {},{}:{}>".format(
            self.fixture_id, self.home_team_id, self.away_team_id,
            self.home_score, self.away_score)

    @classmethod
    def get_by_id(cls, id):
        return cls.session.query(Fixture).filter_by(fixture_id=id).one()

    @classmethod
    def get_past_fixtures(cls, season_id, game_day):
        return (
            cls.session.query(Fixture).filter_by(season_id=season_id)
            .filter(Fixture.game_day < game_day)
            .filter(Fixture.home_score != None)  # noqa
            .filter(Fixture.away_score != None)
            .all()
        )
