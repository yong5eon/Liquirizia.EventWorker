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
from Liquirizia.EventWorker import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
	EventProperties,
)

from Liquirizia.Logger import (
	LOG_INIT,
	LOG_LEVEL_DEBUG,
	LOG_INFO,
	LOG_ERROR,
	LOG_DEBUG,
)

from signal import signal, SIGINT
from random import randint
from time import sleep


class Complete(EventRunnerComplete):
	def __call__(self, completion):
		LOG_INFO('Complete : {}'.format(completion))
		return
	
class Error(EventRunnerError):
	def __call__(self, error: BaseException):
		LOG_ERROR('Error : {}'.format(str(error)), e=error)
		return


@EventProperties(
	event='+',
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {}'.format(a, b))
		return a + b

@EventProperties(
	event='-',
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {}'.format(a, b))
		return a - b

@EventProperties(
	event='*',
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {}'.format(a, b))
		return a * b

@EventProperties(
	event='/',
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {}'.format(a, b))
		return a / b


@EventProperties(
	event='%',
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		return a % b


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
