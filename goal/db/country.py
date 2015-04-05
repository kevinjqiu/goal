from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base


class Country(Base):
    __tablename__ = 'country'
    country_id = Column(String(3), primary_key=True)
    name = Column(String(64), nullable=False)

    competitions = relationship(
        'Competition', uselist=True, backref="country",
        order_by='Competition.tier')

    def __json__(self):
        return {
            'country_id': self.country_id,
            'name': self.name,
        }

    def __repr__(self):
        return "<Country: {},{}>".format(self.country_id, self.name)
