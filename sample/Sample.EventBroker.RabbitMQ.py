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
)
from Liquirizia.EventWorker.Tools.StatusChecker import StatusChecker

from Liquirizia.EventBroker import Helper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
	Consumer,
	Queue,
	EventHandler,
	Event,
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


class SampleEventHandler(EventHandler):
	def __init__(self, pool: Pool):
		self.pool = pool
		return
	def __call__(self, event: Event):
		LOG_INFO('Event : type={}, headers={}, {}'.format(event.type, event.headers(), event.body))
		self.pool.run(
			event=event.type,
			parameters=EventParameters(event.header('c'), **event.body)
		)
		event.ack()
		return


class SampleConsumer(Invoker):
	def __init__(self, pool: Pool):
		self.pool = pool
		self.consumer = None
		return
	def run(self):
		con: Connection = Helper.Get('Sample')
		self.consumer: Consumer = con.consumer(SampleEventHandler(self.pool))
		self.consumer.subs('queue')
		LOG_INFO('Consumer running...')
		self.consumer.run()
		LOG_INFO('Consumer stopped...')
		return
	def stop(self):
		if self.consumer: self.consumer.stop()
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
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def __init__(self, c):
		self.c = c
		return
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {} + {}'.format(a, b, self.c))
		sleep(randint(1, 10))
		return a + b + self.c

@EventProperties(
	event='-',
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def __init__(self, c):
		self.c = c
		return
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {} - {}'.format(a, b, self.c))
		sleep(randint(1, 10))
		return a - b - self.c

@EventProperties(
	event='*',
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def __init__(self, c):
		self.c = c
		return
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {} * {}'.format(a, b, self.c))
		sleep(randint(1, 10))
		return a * b * self.c

@EventProperties(
	event='/',
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def __init__(self, c):
		self.c = c
		return
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {} / {}'.format(a, b, self.c))
		sleep(randint(1, 10))
		return a / b / self.c


@EventProperties(
	event='%',
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def __init__(self, c):
		self.c = c
		return
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {} % {}'.format(a, b, self.c))
		sleep(randint(1, 10))
		return a % b % self.c


if __name__ == '__main__':

	LOG_INIT(LOG_LEVEL_DEBUG, name='Sample.EventBroker.RabbitMQ')

	Helper.Set(
		'Sample',
		Connection,
		Configuration(
			host='127.0.0.1',
			port=5672,
			username='guest',
			password='guest',
		)
	)

	LOG_INFO('EventBroker init...')
	EVENT = ['+', '-', '*', '/', '%']
	con: Connection = Helper.Get('Sample')
	con.createQueue('queue')
	queue: Queue = con.queue('queue')
	for i in range(100):
		event = EVENT[randint(0, 4)]
		a = randint(0, 9)
		b = randint(0, 9)
		c = randint(0, 9)
		queue.send({'a': a, 'b': b}, event=event, headers={'c': c})

	sc = StatusChecker()
	worker = Worker(ThreadPool(), SampleConsumer)
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
	LOG_INFO('EventBroker clean...')
	con.deleteQueue('queue')
