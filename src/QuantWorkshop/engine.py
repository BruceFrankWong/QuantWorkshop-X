# -*- coding: utf-8 -*-

from queue import Queue
from threading import Thread
from time import sleep

from .types import QWEventType, QWEvent, QWCallback


class QWEventEngine(object):
    """A class implement a event loop and a event distribute mechanism.

    The QWEventEngine is the core of the event-driven asynchronous application.
    The event sender(s) call the QWEventEngine.send_event to publish an event
    into QWEventEngine._event_queue, while the event receiver(s) register their
    callback function into event engine. When running, engine pick event from
    the queue, then distribute it by calling the corresponding callback function(s).

    The QWEventEngine contains a timer, generate event by every interval seconds.
    """
    _active: bool            # 引擎开关
    _event_queue: Queue      # 事件队列
    _callback_dict: dict     # 事件回调程序字典
    _event_thread: Thread    # 事件引擎主进程
    _timer_thread: Thread    # 定时器线程
    _timer_interval: int     # 定时器间隔

    def __init__(self, timer_interval: int = 1) -> None:
        self._active = False
        self._event_queue = Queue()
        self._callback_dict = {}
        if timer_interval > 0:
            self._timer_interval = timer_interval
        else:
            self._timer_interval = 1

        self._event_thread = Thread(target=self._run_event_thread, name='EventThread')
        self._timer_thread = Thread(target=self._run_timer_thread, name='TimerThread')

    def _run_timer_thread(self) -> None:
        """Generate the timer event, running in timer thread."""
        while self._active:
            event = QWEvent(type_=QWEventType.TimerEvent,
                            data='TimerTriggered')  # 创建计时器事件
            self.send_event(event)                  # 向队列中存入计时器事件
            sleep(self._timer_interval)             # 等待

    def _run_event_thread(self) -> None:
        """Get event from queue and then distribute it, running in event thread."""
        while self._active:
            if not self._event_queue.empty():
                event = self._event_queue.get(block=True, timeout=1)    # 获取队列中的事件，超时1秒
                self._distribute_event(event)   # 分发事件
            else:
                # print('无任何事件')
                pass

    def _distribute_event(self, event: QWEvent) -> None:
        """Distribute event to each registered callback function by event type.
        :param event:   the event.
        :return: None.
        """
        if event.type_ in self._callback_dict:
            [callback(event) for callback in self._callback_dict[event.type_]]

    def start(self) -> None:
        """Start the event engine to distribute events and generate timer events."""
        self._active = True
        self._event_thread.start()
        self._timer_thread.start()
        event = QWEvent(type_=QWEventType.EngineEvent,
                        data='Engine start.')
        self.send_event(event)

    def stop(self) -> None:
        """Stop the event engine."""
        self._active = False
        event = QWEvent(type_=QWEventType.EngineEvent,
                        data='Engine stop.')
        self.send_event(event)
        self._timer_thread.join()
        self._event_thread.join()

    def register(self, type_: QWEventType, callback: QWCallback) -> None:
        """Register a new callback function for a specific event type.
        Callback function can be registered to receive multi type event, but
        only once for each type.

        :param type_:       the event type that callback function want to register.
        :param callback:    the callback function.

        :return: None.
        """
        if type_ not in self._callback_dict.keys():
            self._callback_dict[type_] = [callback]
        else:
            self._callback_dict[type_].append(callback)

    def unregister(self, type_: QWEventType, callback: QWCallback) -> None:
        """Unregister an existing callback function from event engine.

        :param type_:       the event type that callback function want to unregister.
        :param callback:    the callback function.

        :return: None.
        """
        if type_ not in self._callback_dict.keys():
            raise ValueError('type not in callback list.')
        else:
            if callback in self._callback_dict[type_]:
                self._callback_dict[type_].remove(callback)
            else:
                raise ValueError('callback not registered.')

    def send_event(self, event: QWEvent) -> None:
        """Put an event object into queue.

        :param event:    the event.

        :return: None.
        """
        self._event_queue.put(event)
