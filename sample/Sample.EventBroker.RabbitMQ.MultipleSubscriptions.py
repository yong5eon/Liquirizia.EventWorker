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

from Liquirizia.EventBroker import Helper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
	Consumer,
	Queue,
	EventHandler,
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
	parameters='Q.+',
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {}'.format(a, b))
		sleep(randint(1, 10))
		return a + b

@EventProperties(
	event='-',
	parameters='Q.-',
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {}'.format(a, b))
		sleep(randint(1, 10))
		return a - b

@EventProperties(
	event='*',
	parameters='Q.*',
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {}'.format(a, b))
		sleep(randint(1, 10))
		return a * b

@EventProperties(
	event='/',
	parameters='Q./',
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {}'.format(a, b))
		sleep(randint(1, 10))
		return a / b


@EventProperties(
	event='%',
	parameters='Q.%',
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		sleep(randint(1, 10))
		return a % b


class SampleEventHandler(EventHandler):
	def __init__(self, pool: Pool):
		self.pool = pool
		return
	def __call__(self, event):
		LOG_INFO('Event : type={}, {}'.format(event.type, event.body))
		self.pool.run(
			event=event.type,
			parameters=Parameters(**event.body)
		)
		event.ack()
		return


class SampleConsumer(Invoker):
	def __init__(self, pool: Pool):
		self.pool = pool
		self.consumer = None
		return
	def run(self):
		ctx = Context()
		con: Connection = Helper.Get('Sample')
		self.consumer: Consumer = con.consumer(SampleEventHandler(self.pool))
		for event, queue in ctx.parameters().items():
			LOG_DEBUG('Subscribe : {}'.format(event))
			self.consumer.subs(queue)
		LOG_INFO('Consumer running...')
		self.consumer.run()
		LOG_INFO('Consumer stopped...')
		return
	def stop(self):
		if self.consumer: self.consumer.stop()
		return


if __name__ == '__main__':

	LOG_INIT(LOG_LEVEL_DEBUG)

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

	ctx = Context()

	LOG_INFO('EventBroker init...')
	EVENT = ['+', '-', '*', '/', '%']
	con: Connection = Helper.Get('Sample')

	for k, param in ctx.parameters().items():
		LOG_INFO('Create queue : {}'.format(param))
		con.createQueue(param)

	params = ctx.parameters()
	for i in range(100):
		event = EVENT[randint(0, 4)]
		queue = params[event]
		body = {'a': randint(0, 9), 'b': randint(0, 9)}	
		LOG_DEBUG('Send : event={}, body={} to {}'.format(event, body, queue))
		q: Queue = con.queue(queue)
		q.send(body, event=event)

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
	for k, param in ctx.parameters().items():
		LOG_INFO('Delete queue : {}'.format(param))
		con.deleteQueue(param)
