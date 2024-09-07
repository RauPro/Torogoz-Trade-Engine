import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv

class PlatformConnector():
    def __init__(self, symbol_list: list):
        load_dotenv(find_dotenv())
        self._initialize_platform()
        self._live_account_warning()
        self._check_algo_trading_enable()
        self._add_symbols_to_marketwatch(symbol_list)

    def _initialize_platform(self) -> None:
        """

        :return:
        """
        if mt5.initialize(
            path=os.getenv("MT5_PATH"),
            login=int(os.getenv("MT5_LOGIN")),
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            timeout=int(os.getenv("MT5_TIMEOUT")),
            portable=eval(os.getenv("MT5_PORTABLE"))
        ):
            print("Working Fine")
        else:
            raise Exception("Not Working", mt5.last_error())

    def _live_account_warning(self) -> None:

        if mt5.account_info().trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("Using Demo Account")
        elif mt5.account_info().trade_mode == mt5.ACCOUNT_TRADE_MODE_REAL:
            if not input("Using REAL Account, Confirm to continue (y/n): ").lower() == "y":
                mt5.shutdown()
                raise Exception("Shutting Down")
        else:
            print("Using not consider Real - Demo account")

    def _check_algo_trading_enable(self) -> None:
        if not mt5.terminal_info().trade_allowed:
            raise Exception("Algorithmic trading not enable, active first to use")

    def _add_symbols_to_marketwatch(self, symbols: list) -> None:
        for symbol in symbols:
            if mt5.symbol_info(symbol) is None:
                print("Cannot add Symbol", symbol, "to Market Watch", mt5.last_error())
                continue
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol, True):
                    print("Cannot add Symbol", symbol, "to Market Watch", mt5.last_error())
                else:
                    print("Symbol", symbol, "added successfully")
            else:
                print("Symbol already added to Market Watch")