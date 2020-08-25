#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any
from threading import Thread
from time import sleep
from datetime import datetime

from QuantWorkshop.engine import QWEventEngine
from QuantWorkshop.types import QWEventType, QWEvent


test_event_trigger_count: int = 0


class FakeSender(object):
    def __init__(self,
                 event_engine: QWEventEngine,
                 event_type: QWEventType,
                 event_data: Any,
                 interval: int) -> None:
        self.event_engine: QWEventEngine = event_engine
        self.event_type: QWEventType = event_type
        self.event_data: Any = event_data
        self.interval: int = interval
        self.thread = Thread(target=self.timer)
        self.active: bool = False

    def timer(self):
        while self.active:
            event = QWEvent(type_=self.event_type,
                            data=self.event_data)  # 创建计时器事件
            self.event_engine.send_event(event)  # 向队列中存入计时器事件
            print('[FakeSender]-[{}]: Fake event send.'.format(datetime.now()))
            sleep(self.interval)  # 等待

    def start(self):
        self.active = True
        self.thread.start()

    def stop(self):
        self.active = False
        self.thread.join()


def test_event_engine():
    def test_event_callback(event: QWEvent):
        global test_event_trigger_count

        assert event.data == test_event_data, \
            'QWEvent.data is NOT "TestEvent".'
        test_event_trigger_count += 1
        print('[TestCallback]-[{}]: Test event received. Count = {}'.format(datetime.now(), test_event_trigger_count))
        if test_event_trigger_count == 10:
            fake_sender.stop()
            event_engine.stop()

    def test_timer_callback(event: QWEvent):
        assert event.data == 'TimerTriggered', \
            'QWEvent.data is NOT "TimerTriggered".'
        print('[TimerCallback]-[{}]: Timer event received.'.format(datetime.now()))

    test_event_data: str = 'TestEvent'

    event_engine = QWEventEngine(3)
    assert event_engine._active is False, \
        'EventEngine._active is NOT False.'
    assert event_engine._event_queue.empty(), \
        'EventEngine._event_queue is NOT empty.'
    assert not event_engine._callback_dict, \
        'EventEngine._callback_dict is NOT empty.'
    assert event_engine._event_thread.name == 'EventThread', \
        'EventEngine._event_thread.name is NOT "EventThread".'
    assert event_engine._timer_thread.name == 'TimerThread', \
        'EventEngine._event_thread.name is NOT "EventThread".'
    assert event_engine._timer_interval == 3, \
        'EventEngine._active is NOT equal 3.'

    event_engine = QWEventEngine(-1)
    assert event_engine._timer_interval == 1, \
        'EventEngine._active is NOT equal 1.'

    event_engine = QWEventEngine()
    assert event_engine._timer_interval == 1, \
        'EventEngine._active is NOT equal 1.'

    event_engine.register(QWEventType.TimerEvent, test_timer_callback)
    event_engine.register(QWEventType.UncategorizedEvent, test_event_callback)
    assert len(event_engine._callback_dict.keys()) == 2, \
        'EventEngine._callback_dict ERROR.'
    event_engine.start()

    fake_sender = FakeSender(event_engine=event_engine,
                             event_type=QWEventType.UncategorizedEvent,
                             event_data=test_event_data,
                             interval=2)
    fake_sender.start()


if __name__ == '__main__':
    test_event_engine()
