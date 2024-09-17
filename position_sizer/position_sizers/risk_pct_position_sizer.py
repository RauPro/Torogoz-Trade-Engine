from data_provider.data_provider import DataProvider
from events.events import SignalEvent
from ..interfaces.position_sizer_interface import IPositionSizer
from ..properties.position_sizer_properties import RiskPctSizingProps
from utils.utils import Utils
import MetaTrader5 as mt5


class RiskPctPositionSizer(IPositionSizer):

    def __init__(self, properties: RiskPctSizingProps):
        """
        Initializes a RiskPctPositionSizer object.

        Args:
            properties (RiskPctSizingProps): An object containing the properties for risk percentage position sizing.
        """
        self.risk_pct = properties.risk_pct

    def size_signal(self, signal_event: SignalEvent, data_provider: DataProvider) -> float:
        """
        Calculates the size of the position based on the risk percentage and signal event data.

        Args:
            signal_event (SignalEvent): The signal event containing information about the trade.
            data_provider (DataProvider): The data provider used to retrieve market data.

        Returns:
            float: The size of the position.

        Raises:
            None.
        """
        # Check that the risk is positive
        if self.risk_pct <= 0.0:
            print(
                f"{Utils.dateprint()} - ERROR (RiskPctPositionSizer): The entered risk percentage: {self.risk_pct} is not valid.")
            return 0.0

        # Check that sl != 0
        if signal_event.sl <= 0.0:
            print(f"{Utils.dateprint()} - ERROR (RiskPctPositionSizer): The SL value: {signal_event.sl} is not valid.")
            return 0.0

        # Access account information (to obtain account currency)
        account_info = mt5.account_info()

        # Access symbol information (to calculate risk)
        symbol_info = mt5.symbol_info(signal_event.symbol)

        # Retrieve the estimated entry price:
        # If it is a market order
        if signal_event.target_order == "MARKET":
            # Get the last available market price (ask or bid)
            last_tick = data_provider.get_latest_tick(signal_event.symbol)
            entry_price = last_tick['ask'] if signal_event.signal == "BUY" else last_tick['bid']

        # If it is a pending order (limit or stop)
        else:
            # Take the price from the signal event itself
            entry_price = signal_event.target_price

        # Get the values needed for calculations
        equity = account_info.equity
        volume_step = symbol_info.volume_step  # Minimum volume change
        tick_size = symbol_info.trade_tick_size  # Minimum price change
        account_ccy = account_info.currency  # account currency
        symbol_profit_ccy = symbol_info.currency_profit  # profit currency of the symbol
        contract_size = symbol_info.trade_contract_size  # contract size (e.g., 1 standard lot)

        # Auxiliary calculations
        tick_value_profit_ccy = contract_size * tick_size  # Amount gained or lost per lot and per tick

        # Convert the tick value in profit currency of the symbol to the currency of our account
        tick_value_account_ccy = Utils.convert_currency_amount_to_another_currency(tick_value_profit_ccy,
                                                                                   symbol_profit_ccy, account_ccy)

        # Calculation of the position size
        try:
            price_distance_in_integer_ticksizes = int(abs(entry_price - signal_event.sl) / tick_size)
            monetary_risk = equity * self.risk_pct
            volume = monetary_risk / (price_distance_in_integer_ticksizes * tick_value_account_ccy)
            volume = round(volume / volume_step) * volume_step

        except Exception as e:
            print(f"{Utils.dateprint()} - ERROR: Problem calculating the position size based on risk. Exception: {e}")
            return 0.0

        else:
            return volume
