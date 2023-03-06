import base

from exchange import Exchange
from authentication import authentication
from models import EventType, Event

# Initialize authentication properties and pass them to an Exchange instance
session = authentication.Session()
exchange = Exchange(token=session.token, appkey=session.appkey)

# Generate database schema
# base.Base.metadata.create_all(base.engine)
exchange.base.metadata.create_all(base.engine)

# Create a new session
db_session = base.Session()

# Create EventType objects and queue them for persistence
event_types_raw = exchange.list_event_types()
event_types = [
    EventType(**event_type)
    for event_type in event_types_raw
]
for event_type in event_types:
    db_session.add(event_type)
    print('+ Updating event Type: ', event_type.name)

# Create Event (and encapsulated) objects and queue them for persistence
events_raw = [
    exchange.list_events([str(event_type.id)])
    for event_type in event_types
    if event_type.id == "1"
][0]
print('+ Using ', 'soccer'.upper())
events = [Event(1, token=session.token, appkey=session.appkey, **event) for event in events_raw]
for event in events:
    db_session.add(event)
    for market in event.markets_list:
        db_session.add(market)
        for runner in market.runners_list:
            db_session.add(runner)

# Commit and close the session
db_session.commit()
db_session.close()
