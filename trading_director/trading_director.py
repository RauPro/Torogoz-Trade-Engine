# QUANTDEMY - https://quantdemy.com - Trading con Python y MetaTrader 5: Crea tu Propio Framework

from data_provider.data_provider import DataProvider
from typing import Dict, Callable
import queue
import time

from events.events import *


class TradingDirector():

    def __init__(self, events_queue: queue.Queue, data_provider: DataProvider):
        """
        Initializes the TradingDirector object.

        Args:
            events_queue (queue.Queue): The queue to receive events.
            data_provider (DataProvider): The data provider object.
            signal_generator (ISignalGenerator): The signal generator object.
            position_sizer (PositionSizer): The position sizer object.
            risk_manager (RiskManager): The risk manager object.
            order_executor (OrderExecutor): The order executor object.
            notification_service (NotificationService): The notification service object.
        """
        self.events_queue = events_queue
        self.DATA_PROVIDER = data_provider
        self.continue_trading: bool = True
        self.event_handler: Dict[str, Callable] = {
            "DATA": self._handle_data_event,
            "SIGNAL": self._handle_signal_event,
            "SIZING": self._handle_sizing_event,
            "ORDER": self._handle_order_event,
            "EXECUTION": self._handle_execution_event,
            "PENDING": self._handle_pending_order_event
        }

    def _handle_data_event(self, event: DataEvent):
        """
        Handle the data event.

        Args:
            event (DataEvent): The data event object.

        Returns:
            None
        """
        print(
            f"Received DATA EVENT of {event.symbol} - last closed price: {event.data.close}")
        #self.SIGNAL_GENERATOR.generate_signal(event)

    def _handle_signal_event(self, event: SignalEvent):
        """
        Handle the signal event.

        Args:
            event (SignalEvent): The signal event object.

        Returns:
            None
        """
        # Procesamos el signal event
        print(f"Recibido SIGNAL EVENT {event.signal} para {event.symbol}")
        #self.POSITION_SIZER.size_signal(event)

    def _handle_sizing_event(self, event: SizingEvent):
        """
        Handle the sizing event.

        Args:
            event (SizingEvent): The sizing event object.

        Returns:
            None
        """
        print(
            f"Recibido SIZING EVENT con volumen {event.volume} para {event.signal} en {event.symbol}")
        #self.RISK_MANAGER.assess_order(event)

    def _handle_order_event(self, event: OrderEvent):
        """
        Handle the order event.

        Args:
            event (OrderEvent): The order event object.

        Returns:
            None
        """
        print(
            f"Received ORDER EVENT con with volume {event.volume} for {event.signal} in {event.symbol}")
        #self.ORDER_EXECUTOR.execute_order(event)

    def _handle_execution_event(self, event: ExecutionEvent):
        """
        Handle the execution event.

        Args:
            event (ExecutionEvent): The execution event object.

        Returns:
            None
        """
        print(
            f"Received EXECUTION EVENT {event.signal} in {event.symbol} with volume {event.volume} with price {event.fill_price}")
        #self._process_execution_or_pending_events(event)

    def _handle_pending_order_event(self, event: PlacedPendingOrderEvent):
        """
        Handle the pending order event.

        Args:
            event (PlacedPendingOrderEvent): The pending order event object.

        Returns:
            None
        """
        print(
            f"Received PLACED PENDING ORDER EVENT with volume {event.volume} for {event.signal} {event.target_order} in {event.symbol} with price {event.target_price}")
        #self._process_execution_or_pending_events(event)



    def _handle_none_event(self, event):
        """
        Handles the case when a None event is received.

        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.

        Args:
            event: The None event received.
        """
        print(f"ERROR: Null event received. Terminating execution of the Framework. Event: {event}")
        self.continue_trading = False

    def _handle_unknown_event(self, event):
        """
        Handles the case when an Unknown event is received.

        Prints an error message and sets `continue_trading` flag to False, terminating the execution of the Framework.

        Args:
            event: The Unknown event received.
        """
        print(
            f"ERROR: Unknown event received. Terminating execution of the Framework. Event: {event}")
        self.continue_trading = False

    def execute(self) -> None:
        """
        Executes the main trading loop.

        This method continuously checks for events in the events queue and handles them accordingly.
        If no events are available, it checks for new data from the data provider.
        The loop continues until the `continue_trading` flag is set to False.

        Note:
        - The events are processed by the corresponding event handlers.
        - If an unknown event is encountered, it is handled by the `_handle_unknown_event` method.
        - If a None event is encountered, it is handled by the `_handle_none_event` method.

        Returns:
        None
        """
        while self.continue_trading:
            try:
                event = self.events_queue.get(block=False)
            except queue.Empty:
                self.DATA_PROVIDER.check_for_new_data()
            else:
                if event is not None:
                    handler = self.event_handler.get(event.event_type, self._handle_unknown_event)
                    handler(event)
                else:
                    self._handle_none_event(event)
            time.sleep(0.01)
        print(f"Ending")
