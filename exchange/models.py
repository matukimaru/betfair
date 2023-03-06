from exchange import Exchange
from base import Base

from sqlalchemy.types import Float
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import relationship

dt_format = '%Y-%m-%dT%H:%M:%SZ'


class EventType(Base):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(200))
    market_count = Column(Integer)

    events = relationship('Event')

    def __init__(self, **kwargs):
        self.id = kwargs['eventType']['id']
        self.name = kwargs['eventType']['name']
        self.market_count = kwargs['marketCount']


class Event(Base):
    """
    Todo: Figure out a way of getting the most traded markets for every event: maybe top-5
    """
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(200))
    country_code = Column(String(50))
    timezone = Column(String(200))
    open_date = Column(String(100))
    market_count = Column(Integer)

    event_type_id = Column(Integer, ForeignKey('event_types.id'))

    markets = relationship('Market')

    def __init__(self, et_id, token, appkey, **kwargs):
        self.exchange = Exchange(token=token, appkey=appkey)
        self.id = kwargs['event']['id']
        self.name = kwargs['event']['name']
        try:
            self.country_code = kwargs['event']['countryCode']
        except KeyError:
            self.country_code = ''
        self.timezone = kwargs['event']['timezone']
        self.open_date = kwargs['event']['openDate']
        self.market_count = kwargs['marketCount']
        self.markets_list = []
        self.event_type_id = et_id
        print('  + creating event: ', self.name)
        # Get market catalogue
        # Filter out to the two interesting ones
        # Initialize markets
        catalogue = self.exchange.list_market_catalogue(self.id)
        for market in catalogue:
            # if market['marketName'] == 'Match Odds':
            #     self.markets_list.append(Market(self.id, self.exchange, **market))
            if market['marketName'] == 'Over/Under 2.5 Goals':
                self.markets_list.append(Market(self.id, self.exchange, **market))
            # if market['marketName'] == 'Half Time':
            #     self.markets_list.append(Market(self.id, self.exchange, **market))
            else:
                continue


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Float(precision=32), primary_key=True, autoincrement=False)
    name = Column(String(200))
    total_matched = Column(Numeric)

    event_id = Column(BigInteger, ForeignKey('events.id'))

    runners = relationship('Runner')

    def __init__(self, eid, exchange, **kwargs):
        self.exchange = exchange
        self.id = kwargs['marketId']
        self.name = kwargs['marketName']
        self.total_matched = kwargs['totalMatched']
        self.event_id = eid
        self.runners_list = []
        print('    - attaching market: ', self.name)
        for value in kwargs['runners']:  # Shows the selection ID and runner name [eg: home win, away win, draw]
            selection_id = value['selectionId']  # Same as runner id
            runner_name = value['runnerName']
            # Get the runner book for this particular selection ID
            runner_book = self.exchange.list_runner_book(self.id, selection_id)[0]['runners'][0]
            # Instantiate a runner object and add it to this object's runners list
            self.runners_list.append(Runner(self.id, selection_id, runner_name, **runner_book))


class Runner(Base):
    __tablename__ = 'runners'

    number = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    price = Column(Float)
    size = Column(Numeric)

    market_id = Column(Float(precision=32), ForeignKey('markets.id'))

    def __init__(self, mk_id, selection_id, runner_name, **kwargs):
        self.id = selection_id
        self.name = runner_name
        try:
            control_value = kwargs['ex']['availableToBack'][0]['size']
            for avb in kwargs['ex']['availableToBack']:  # Pick the best back match - by largest size
                if avb['size'] > control_value:
                    self.price = avb['price']
                    self.size = avb['size']
            self.market_id = mk_id
            print('      ... attaching runner: ', self.name)
        except IndexError:
            pass
