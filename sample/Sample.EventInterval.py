# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	Worker,
	Invoker,
	Pool,
	ThreadPool,
	ProcessPool,
	EventProperties,
	EventParameters,
	EventRunner,
	EventComplete,
	EventError,
	EventContext,
)
from Liquirizia.EventWorker.Tools.StatusChecker import StatusChecker

from Liquirizia.Logger import (
	LOG_INIT,
	LOG_LEVEL_DEBUG,
	LOG_INFO,
	LOG_ERROR,
	LOG_DEBUG,
)

from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import get_context
from signal import signal, SIGINT
from random import randint
from time import sleep


class SampleEventInvoker(Invoker):
	def __init__(self, pool: Pool):
		self.event = get_context().Manager().Event()
		self.pool = pool
		self.sched = BackgroundScheduler(timezone='Asia/Seoul')
		return
	def invoke(self, event: str):
		a = randint(0, 9)
		b = randint(0, 9)
		LOG_INFO('Event : type={}, {}'.format(a, {'a': a, 'b': b}))
		self.pool.run(
			event=event,
			parameters=EventParameters(**{'a': a, 'b': b}),
		)
		return

	def run(self):
		ctx = EventContext()	
		for event, interval in ctx.events().items():
			LOG_DEBUG('Create event : event={}, interval={}'.format(event, interval))
			self.sched.add_job(
				self.invoke,
				'interval',
				seconds=interval,
				args=(event,),
			)
		self.sched.start()
		while not self.event.is_set():
			sleep(1)
		return
	
	def stop(self):
		self.sched.shutdown()
		self.event.set()
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
	properties=2,
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
	properties=3,
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
	properties=4,
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
	properties=5,
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
	properties=6,
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		sleep(randint(1, 5))
		return a % b


if __name__ == '__main__':
	LOG_INIT(LOG_LEVEL_DEBUG, name='Sample.EventInterval')
	sc = StatusChecker()
	worker = Worker(ThreadPool(), SampleEventInvoker)
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
