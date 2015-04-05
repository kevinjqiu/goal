from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Team(Base):
    __tablename__ = 'team'
    team_id = Column(String(6), primary_key=True)
    country_id = Column(
        String(3), ForeignKey('country.country_id'), nullable=False)
    name = Column(String(64), nullable=False)
    current_competition_id = Column(
        String(10), ForeignKey('competition.competition_id'))

    country = relationship('Country', uselist=False)
    current_competition = relationship(
        'Competition', backref="current_teams",
        uselist=False)

    def __repr__(self):
        return "<Team: {},{}>".format(self.team_id, self.name)

    def __json__(self):
        return {
            "id": self.team_id,
            "country_id": self.country_id,
            "name": self.name,
            "current_competition_id": self.current_competition_id,
        }

    @classmethod
    def get_by_id(cls, id):
        return Team.session.query(Team).filter_by(team_id=id).one()
