import requests
import json

from data_filter import DataFilter

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Exchange:

    def __init__(self, token=None, appkey=None):
        self.__token = token
        self.__appkey = appkey
        self.__data = ''
        self.__headers = ''
        self.__operation = ''  # Such as 'listEventTypes'
        self.__endpoint = 'https://api.betfair.com/exchange/betting/rest/v1.0/'
        self.df = DataFilter()  # To build filters from within this class
        self.__engine = create_engine("mysql://root:passpass@localhost/betfair")
        self.__db_session = sessionmaker(bind=self.__engine)
        self.__base = declarative_base()

    @property
    def engine(self):
        return self.__engine

    @property
    def db_session(self):
        return self.__db_session

    @property
    def base(self):
        return self.__base

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def appkey(self):
        return self.__appkey

    @appkey.setter
    def appkey(self, value):
        self.__appkey = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def headers(self):
        return {'X-Application': self.appkey, 'X-Authentication': self.token,
                'content-type': 'application/json'}

    @headers.setter
    def headers(self, value):
        self.__headers = value

    @property
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, value):
        self.__endpoint = value

    @property
    def operation(self):
        return self.__operation

    @operation.setter
    def operation(self, value):
        self.__operation = value

    @property
    def response(self):
        return requests.post(self.endpoint + self.operation, data=self.data, headers=self.headers).text

    def list_event_types(self):
        """
        List< EventTypeResult > listEventTypes ( MarketFilter filter ,Stringlocale ) throws APINGException
        Returns a list of Event Types (i.e. Sports) associated with the markets selected by the MarketFilter.

        :return:
        """
        self.operation = 'listEventTypes/'
        self.data = self.df.df_list_event_types()
        return json.loads(self.response)

    def list_events(self, evt_ids):
        """
        List< EventResult > listEvents ( MarketFilter filter ,Stringlocale ) throws APINGException
        Returns a list of Events (i.e, Reading vs. Man United) associated with the markets selected by the MarketFilter.

        :param evt_ids: A list of Event Type Ids (type str)
        :return:
        """
        self.operation = 'listEvents/'
        self.data = self.df.df_list_events(evt_ids)
        return json.loads(self.response)

    def list_market_catalogue(self, ev_ids):
        """
        List< MarketCatalogue > listMarketCatalogue ( MarketFilter filter ,Set< MarketProjection >marketProjection,
        MarketSort sort, intmaxResults ,Stringlocale ) throws APINGException.

        Returns a list of information about published (ACTIVE/SUSPENDED) markets that does not change
        (or changes very rarely). You use listMarketCatalogue to retrieve the name of the market, the names of
        selections and other information about markets.  Market Data Request Limits apply to requests made to
        listMarketCatalogue.

        Please note: listMarketCatalogue does not return markets that are CLOSED.
        Calls to listMarketBook should be made up to a maximum of 5 times per second to a single marketId.

        :param ev_ids:
        :return:
        """
        self.operation = 'listMarketCatalogue/'
        self.data = self.df.df_list_market_catalogue(ev_ids)
        return json.loads(self.response)

    def list_runner_book(self, mk_id, sel_id):
        """
        List<MarketBook> listRunnerBook ( MarketId marketId, SelectionId selectionId, double handicap, PriceProjection
        priceProjection, OrderProjection orderProjection, MatchProjection matchProjection, boolean
        includeOverallPosition, boolean partitionMatchedByStrategyRef, Set<String> customerStrategyRefs,
        StringcurrencyCode,Stringlocale, Date matchedSince, Set<BetId> betIds) throws APINGException

        Returns a list of dynamic data about a market and a specified runner. Dynamic data includes prices, the status
        of the market, the status of selections, the traded volume, and the status of any orders you have placed in the
        market..

        You can only pass in one marketId and one selectionId in that market per request. If the selectionId being
        passed in is not a valid one / doesn’t belong in that market then the call will still work but only the market
        data is returned.

        :param mk_id:
        :param sel_id:
        :return:
        """
        self.operation = 'listRunnerBook/'
        self.data = self.df.df_list_runner_book(mk_id, sel_id)
        return json.loads(self.response)
