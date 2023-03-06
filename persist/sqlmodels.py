from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class EventType(Base):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    market_count = Column(Integer)

    events = relationship('Event')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_code = Column(String)
    time_zone = Column(String)
    open_date = Column(DateTime)
    market_count = Column(Integer)

    event_type_id = Column(Integer, ForeignKey('event_types.id'))

    markets = relationship('Market')


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Float, primary_key=True)
    name = Column(String)
    total_matched = Column(Float)

    event_id = Column(Integer, ForeignKey('events.id'))

    runners = relationship('Runner')


class Runner(Base):
    __tablename__ = 'runners'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    market_id = Column(Float, ForeignKey('markets.id'))

    ex = relationship('Ex')


class Ex(Base):
    __tablename__ = 'ex'

    back_price = Column(Float)
    back_size = Column(Float)
    lay_price = Column(Float)
    lay_size = Column(Float)

    runner_id = Column(Integer, ForeignKey('runners.id'))
