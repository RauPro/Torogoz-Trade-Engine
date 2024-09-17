import MetaTrader5 as mt5
from datetime import datetime, timezone
from backports.zoneinfo import ZoneInfo


# Create a static method to convert one currency to another
class Utils():

    def __init__(self):
        """
        Initializes the object.
        """
        pass

    # We create our static method with the @staticmethod decorator
    @staticmethod
    def convert_currency_amount_to_another_currency(amount: float, from_ccy: str, to_ccy: str) -> float:
        """
        Converts the given amount from one currency to another.

        Args:
            amount (float): The amount to be converted.
            from_ccy (str): The currency code of the source currency.
            to_ccy (str): The currency code of the target currency.

        Returns:
            float: The converted amount.

        Raises:
            Exception: If the symbol is not available in the MT5 platform.
        """
        # Check if both currencies for conversion are the same
        if from_ccy == to_ccy:
            return amount

        all_fx_symbol = (
        "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
        "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
        "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY", "USDSEK", "USDNOK")

        # Convert currencies to uppercase
        from_ccy = from_ccy.upper()
        to_ccy = to_ccy.upper()

        # Find the symbol that relates our source currency to our target currency (list comprehension)
        fx_symbol = [symbol for symbol in all_fx_symbol if from_ccy in symbol and to_ccy in symbol][0]
        fx_symbol_base = fx_symbol[:3]

        # Retrieve the latest available data for fx_symbol
        try:
            tick = mt5.symbol_info_tick(fx_symbol)
            if tick is None:
                raise Exception(
                    f"The symbol {fx_symbol} is not available on the MT5 platform. Please check the available symbols from your broker.")

        except Exception as e:
            print(
                f"ERROR: Could not retrieve the last tick for symbol {fx_symbol}. MT5 error: {mt5.last_error()}, Exception: {e}")
            return 0.0

        else:
            # Retrieve the last available price for the symbol
            last_price = tick.bid

            # Convert the amount from the source currency to the target currency
            converted_amount = amount / last_price if fx_symbol_base == to_ccy else amount * last_price
            return converted_amount

    @staticmethod
    def dateprint() -> str:
        """
        Returns the current date and time in the format "dd/mm/yyyy HH:MM:SS.sss".
        The timezone used is "Asia/Nicosia".
        """
        return datetime.now(ZoneInfo("Asia/Nicosia")).strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
