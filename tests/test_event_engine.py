#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from QuantWorkshop.engine import QWEventEngine
from QuantWorkshop.types import QWEventType, QWEvent


class QWMultiThreadingEventEngineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.event_engine = QWEventEngine()

    def tearDown(self) -> None:
        self.event_engine.stop()

    def timer_callback(self, event: QWEvent):
        self. assertEqual('TimerTriggered', event.data)

    def test_timer_should_callback(self):
        self.event_engine.register(QWEventType.TimerEvent, self.timer_callback)
        self.event_engine.start()


if __name__ == '__main__':
    unittest.main()
