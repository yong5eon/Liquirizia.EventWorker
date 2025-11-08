# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	Worker,
	Invoker,
	Pool,
	Setup as BaseSetup,
	ThreadPool,
	ProcessPool,
)
from Liquirizia.EventWorker.Tools.StatusChecker import StatusChecker
from Liquirizia.EventWorker import (
	EventRunner,
	EventParameters,
	EventSetup,
	EventComplete,
	EventError,
	EventProperties,
	EventContext,
	Factory,
)

from Liquirizia.Logger import (
	LOG_INIT,
	LOG_LEVEL_DEBUG,
	LOG_INFO,
	LOG_ERROR,
	LOG_DEBUG,
)

from multiprocessing import get_context
from signal import signal, SIGINT
from random import randint
from time import sleep


class SampleInvoker(Invoker):
	def __init__(self, pool: Pool):
		self.event = get_context().Manager().Event()
		self.pool = pool
		self.context = EventContext()
		return
	def run(self):
		EVENT = ['+', '-', '*', '/', '%']
		while not self.event.is_set():
			event = EVENT[randint(0, 4)]
			a = randint(0, 9)
			b = randint(0, 9)
			LOG_INFO('Event : type={}, {}'.format(event, {'a': a, 'b': b}))
			tid = self.pool.run(
				event=event,
				parameters=EventParameters(**{'a': a, 'b': b}),
			)
			if not tid:
				LOG_ERROR('Event run failed : type={}, {}'.format(event, {'a': a, 'b': b}))
			sleep(1)
		return
	def stop(self):
		self.event.set()
		return


class Init(BaseSetup):
	def __call__(self):
		LOG_INIT(LOG_LEVEL_DEBUG)
		LOG_INFO('Process Initialized')
		return


class Setup(EventSetup):
	def __call__(self, parameters: EventParameters):
		LOG_DEBUG('Setup : parameters={}'.format(parameters))
		return


class Complete(EventComplete):
	def __call__(self, parameters: EventParameters, completion):
		LOG_INFO('Complete : parameters={}, completion={}'.format(parameters, completion))
		return


class Error(EventError):
	def __call__(self, parameters: EventParameters, error: BaseException):
		LOG_ERROR('Error : parameters={}, error={}'.format(parameters, str(error)), e=error)
		return


@EventProperties(
	event='+',
	setups=Setup(),
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {}'.format(a, b))
		sleep(randint(1, 5))
		return a + b

@EventProperties(
	event='-',
	setups=Setup(),
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {}'.format(a, b))
		sleep(randint(1, 5))
		return a - b

@EventProperties(
	event='*',
	setups=Setup(),
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {}'.format(a, b))
		sleep(randint(1, 5))
		return a * b

@EventProperties(
	event='/',
	setups=Setup(),
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {}'.format(a, b))
		sleep(randint(1, 5))
		return a / b


@EventProperties(
	event='%',
	setups=Setup(),
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		sleep(randint(1, 5))
		return a % b

if __name__ == '__main__':
	LOG_INIT(LOG_LEVEL_DEBUG)
	sc = StatusChecker()
	# 멀티쓰레딩 워커를 사용을 원하면 아래 주석을 해제하세요.
	worker = Worker(ThreadPool(), SampleInvoker)
	# 멀티프로세싱 워커를 사용을 원하면 아래 주석을 해제하세요.
	# worker = Worker(ProcessPool(setups=Init()), SampleInvoker)
	def stop(signal, frame):
		LOG_INFO('EventWorker stopping...')
		worker.stop()
		sc.stop()
		return
	signal(SIGINT, stop)
	LOG_INFO('EventWorker running until break with keyboard interrupt...')
	sc.start()
	worker.run()
	LOG_INFO('EventWorker stopped...')
