from queue import Queue

from data_provider.data_provider import DataProvider
from platform_connector.platform_connector import PlatformConnector
from signal_generator.properties.signal_generator_properties import MACrossoverProps
from signal_generator.signal_generator import SignalGenerator
from signal_generator.signals.signal_ma_crossover import SignalMACrossover
from trading_director.trading_director import TradingDirector

if  __name__ == '__main__':
    symbols = ["AUDCAD", "EURUSD", "USDCHF"]
    timeframe = "1min"
    magic_number = 12345

    mac_props = MACrossoverProps(timeframe=timeframe,
                                 fast_period=5,
                                 slow_period=10)
    events_deque = Queue()
    CONNECT = PlatformConnector(symbol_list=symbols)
    DATA_PROVIDER = DataProvider(events_queue=events_deque, symbol_list=symbols, timeframe=timeframe)
    SIGNAL_GENERATOR = SignalGenerator(events_queue=events_deque,
                                       data_provider=DATA_PROVIDER,
                                       signal_properties=mac_props)

    TRADING_DIRECTOR = TradingDirector(events_queue=events_deque, data_provider=DATA_PROVIDER,
                                       signal_generator=SIGNAL_GENERATOR)
    TRADING_DIRECTOR.execute()