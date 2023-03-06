from datetime import datetime, timedelta
from pytz import timezone


class DataFilter:
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    prefix = '{"filter":{'
    suffix = '}'

    def __init__(self):
        """
        Using one day intervals for now.
        """
        self.__market_start_time = {
            'from': datetime.now(timezone('Africa/Nairobi')).strftime(self.fmt),
            'to': (datetime.now(timezone('Africa/Nairobi')) + timedelta(days=0, hours=5)).strftime(self.fmt)
        }

    @property
    def market_start_time(self):
        return self.__market_start_time

    @market_start_time.setter
    def market_start_time(self, delta):
        """
        Allow the operator to set a time interval.
        :param delta:
        :return:
        """
        self.__market_start_time = {
            'from': datetime.now(timezone('Africa/Nairobi')).strftime(self.fmt),
            'to': (datetime.now(timezone('Africa/Nairobi')) + timedelta(days=delta)).strftime(self.fmt)
        }

    def df_list_event_types(self):
        return self.prefix + self.suffix * 2

    def df_list_events(self, evt_ids):
        """
        Single quotations within the filter throws an exception. Using replace to swap with double quotation marks.
        :param evt_ids:
        :return:
        """
        return (
                self.prefix + '"eventTypeIds":' + str(evt_ids).replace("'", '"') +
                ',"marketStartTime":' + str(self.market_start_time).replace("'", '"') + self.suffix * 2
        )

    def df_list_market_catalogue(self, ev_id):
        """
        :param ev_id:
        :return:
        """
        return (
                self.prefix + '"eventIds":["' + str(ev_id).replace("'", '"') + '"]' + self.suffix +
                ',"sort":"MAXIMUM_TRADED","maxResults":"1000","marketProjection":["RUNNER_METADATA"]' +
                self.suffix
        )

    def df_list_runner_book(self, mk_id, sel_id):
        return (
                '{"marketId":"' + str(mk_id).replace("'", '"') +
                '","selectionId":"' + str(sel_id).replace("'", '"') +
                '","priceProjection":{"priceData":["EX_BEST_OFFERS"]},"orderProjection":"EXECUTABLE","matchProjection":'
                '"ROLLED_UP_BY_AVG_PRICE"' +
                self.suffix
        )
