# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	EventWorkerContext,
	EventWorker,
	EventInvoker,
	EventRunnerPool,
	EventParameters,
	ThreadEventRunnerPool,
	ProcessEventRunnerPool,
)

from SampleEventRunner import *

from Liquirizia.Logger import (
	LOG_INIT,
	LOG_LEVEL_DEBUG,
	LOG_INFO,
)

from signal import signal, SIGINT
from time import sleep
from random import randint


class SampleEventInvoker(EventInvoker):
	def __init__(self, context: EventWorkerContext, pool: EventRunnerPool):
		self.context = context
		self.pool = pool
		return
	def run(self):
		EVENT = ['+', '-', '*', '/', '%']
		while self.context:
			event = EVENT[randint(0, 4)]
			a = randint(0, 9)
			b = randint(0, 9)
			LOG_INFO('Event : type={}, {}'.format(a, {'a': a, 'b': b}))
			self.pool.run(
				event=event,
				parameters=EventParameters(**{'a': a, 'b': b}),
			)
			sleep(1)
		return
	def stop(self):
		pass


if __name__ == '__main__':
	LOG_INIT(LOG_LEVEL_DEBUG)
	worker = EventWorker(ThreadEventRunnerPool(), SampleEventInvoker)
	def stop(signal, frame):
		LOG_INFO('EventWorker stopping...')
		worker.stop()
		return
	signal(SIGINT, stop)
	LOG_INFO('EventWorker running until break with keyboard interrupt...')
	worker.run()
	LOG_INFO('EventWorker stopped...')
