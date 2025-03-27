# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	Worker,
	Invoker,
	Pool,
	ThreadPool,
	ProcessPool,
	Parameters,
	Context,
	EventProperties,
	EventRunner,
	EventComplete,
	EventError,
)
from Liquirizia.EventWorker.Extends.StatusChecker import StatusChecker

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


class Complete(EventComplete):
	def __call__(self, completion, a, b):
		LOG_INFO('Complete : a={}, b={}, completion={}'.format(a, b, completion))
		return
	
class Error(EventError):
	def __call__(self, error: BaseException, a, b):
		LOG_ERROR('Error : a={}, b={}, error={}'.format(a, b, str(error)), e=error)
		return


@EventProperties(
	event='+',
	parameters='*/2 * * * * *',
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
	parameters='*/3 * * * * *',
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
	parameters='*/4 * * * * *',
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
	parameters='*/5 * * * * *',
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
	parameters='*/6 * * * * *',
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		sleep(randint(1, 5))
		return a % b


class SampleInvoker(Invoker):
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
		ctx = Context()	
		for event, param in ctx.parameters().items():
			second, minute, hour, month, day_of_week, year = param.split(' ')
			LOG_DEBUG('Create event : event={}, second={}, minute={}, hour={}, month={}, day_of_week={}, year={}'.format(event, second, minute, hour, month, day_of_week, year))
			self.sched.add_job(
				self.invoke,
				'cron',
				second=second,
				minute=minute,
				hour=hour,
				month=month,
				day_of_week=day_of_week,
				year=year,
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
	sc = StatusChecker()
	worker = Worker(ThreadPool(), SampleInvoker)
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
