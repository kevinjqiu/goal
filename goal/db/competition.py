from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Competition(Base):
    __tablename__ = 'competition'
    competition_id = Column(String(10), primary_key=True)
    country_id = Column(
        String(3), ForeignKey('country.country_id'), nullable=False)
    name = Column(String(64), nullable=False)
    tier = Column(Integer)
    promotion_to = Column(Integer, ForeignKey('competition.competition_id'))
    relegation_to = Column(Integer, ForeignKey('competition.competition_id'))
    num_promoted = Column(Integer)
    num_relegated = Column(Integer)

    seasons = relationship(
        'Season', uselist=True, backref="competition",
        order_by='Season.start_year')

    higher_tier_competition = relationship(
        'Competition', foreign_keys=[relegation_to])
    lower_tier_competition = relationship(
        'Competition', foreign_keys=[promotion_to])

    def __json__(self):
        return {
            'id': self.competition_id,
            'country_id': self.country_id,
            'name': self.name,
            'tier': self.tier,
        }

    def __repr__(self):
        return "<Competition: {},{}>".format(self.competition_id, self.name)

    @classmethod
    def get_by_id(cls, competition_id):
        return (
            cls.session.query(Competition)
            .filter_by(competition_id=competition_id)
            .one()
        )
