#  -*- coding: utf-8 -*-

from typing import Any, Callable
from enum import Enum


class QWEventType(Enum):
    """
    Type of event.
    """
    UncategorizedEvent = 'UncategorizedEvent'   # 未分类事件
    EngineEvent = 'EngineEvent'                 # 引擎事件
    LogEvent = 'LogEvent'                       # log事件
    TimerEvent = 'TimerEvent'                   # 定时器事件
    TickEvent = 'TickEvent'                     # tick事件
    BarEvent = 'BarEvent'                       # bar事件
    TradeEvent = 'TradeEvent'
    OrderEvent = 'OrderEvent'
    PositionEvent = 'PositionEvent'
    AccountEvent = 'AccountEvent'
    ContractEvent = 'ContractEvent'


class QWEvent:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """
    _type: QWEventType
    _data: Any

    def __init__(self, type_: QWEventType, data: Any = None):
        """"""
        self._type = type_
        self._data = data

    @property
    def type_(self) -> QWEventType:
        return self._type

    @property
    def data(self) -> Any:
        return self._data


QWCallback = Callable[[QWEvent], None]
