#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from QuantWorkshop.engine import QWEventEngine
from QuantWorkshop.types import QWEventType, QWEvent


# TODO: How to test a event loop?
class QWMultiThreadingEventEngineTestCase(unittest.TestCase):
    timer_callback_counter: int

    def setUp(self) -> None:
        self.event_engine = QWEventEngine()
        self.timer_callback_counter = 0

    def tearDown(self) -> None:
        self.event_engine.stop()

    def timer_callback(self, event: QWEvent):
        self.assertEqual('TimerTriggered', event.data)
        self.timer_callback_counter += 1
        self.assertEqual(1, self.timer_callback_counter, 'timer_callback called more than one times.')

    def test_timer_should_callback(self):
        self.event_engine.register(QWEventType.TimerEvent, self.timer_callback)
        self.event_engine.start()


if __name__ == '__main__':
    unittest.main()
