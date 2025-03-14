# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	Worker,
	Invoker,
	Pool,
	ThreadPool,
	ProcessPool,
	Parameters,
	EventContext,
	EventProperties,
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)

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
	parameters=2,
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {}'.format(a, b))
		return a + b

@EventProperties(
	event='-',
	parameters=3,
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {}'.format(a, b))
		return a - b

@EventProperties(
	event='*',
	parameters=4,
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {}'.format(a, b))
		return a * b

@EventProperties(
	event='/',
	parameters=5,
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {}'.format(a, b))
		return a / b


@EventProperties(
	event='%',
	parameters=6,
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		return a % b


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
			parameters=Parameters(**{'a': a, 'b': b}),
		)
		return

	def run(self):
		ctx = EventContext()	
		for event, interval in ctx.parameters().items():
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


if __name__ == '__main__':
	LOG_INIT(LOG_LEVEL_DEBUG)
	worker = Worker(ThreadPool(), SampleEventInvoker)
	def stop(signal, frame):
		LOG_INFO('EventWorker stopping...')
		worker.stop()
		return
	signal(SIGINT, stop)
	LOG_INFO('EventWorker running until break with keyboard interrupt...')
	worker.run()
	LOG_INFO('EventWorker stopped...')
