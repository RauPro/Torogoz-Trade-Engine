from queue import Queue

from data_provider.data_provider import DataProvider
from platform_connector.platform_connector import PlatformConnector
from trading_director.trading_director import TradingDirector

if  __name__ == '__main__':
    symbols = ["AUDCAD", "EURUSD", "USDCHF"]
    timeframe = "1min"
    events_deque = Queue()
    CONNECT = PlatformConnector(symbol_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_deque, symbol_list=symbols, timeframe=timeframe)
    TRADING_DIRECTOR = TradingDirector(events_queue=events_deque, data_provider=DATA_PROVIDER)
    TRADING_DIRECTOR.execute()