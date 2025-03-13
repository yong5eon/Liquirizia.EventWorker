# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	EventWorkerContext,
	EventWorker,
	EventInvoker,
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
	EventProperties,
	EventRunnerPool,
	EventParameters,
	ThreadEventRunnerPool,
	ProcessEventRunnerPool,
)

from Liquirizia.EventBroker import Helper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
	Consumer,
	Queue,
	EventHandler,
) 

from signal import signal, SIGINT
from time import sleep
from random import randint


class SampleEventRunnerComplete(EventRunnerComplete):
	def __call__(self, completion):
		print('Complete : {}'.format(completion))
		return
	
class SampleEventRunnerError(EventRunnerError):
	def __call__(self, error: BaseException):
		print('Error : {}'.format(str(error)))
	

@EventProperties(
	event='SampleEvent',
	completes=SampleEventRunnerComplete(),
	errors=SampleEventRunnerError(),
)
class SampleEventRunner(EventRunner):
	def run(self, body):
		print('Run : {}'.format(body))
		if body % 2 == 0:
			raise ValueError('Even number')
		return body
	

class SampleEventHandler(EventHandler):
	def __init__(self, pool: EventRunnerPool):
		self.pool = pool
		return
	def __call__(self, event):
		print('Event : {}'.format(event.body))
		self.pool.run(
			event='SampleEvent',
			parameters=EventParameters(event.body)
		)
		event.ack()
		return


class SampleEventConsumer(EventInvoker):
	def __init__(self, context: EventWorkerContext, pool: EventRunnerPool):
		self.context = context
		self.pool = pool
		self.consumer = None
		return
	def run(self):
		con: Connection = Helper.Get('Sample')
		self.consumer: Consumer = con.consumer(SampleEventHandler(self.pool))
		self.consumer.subs('queue')
		print('Consumer running...')
		self.consumer.run()
		print('Consumer stopped...')
		return
	def stop(self):
		if self.consumer:
			self.consumer.stop()
		return


if __name__ == '__main__':

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

	print('EventBroker init...')
	con: Connection = Helper.Get('Sample')
	con.createQueue('queue')
	queue: Queue = con.queue('queue')
	for i in range(10):
		v = randint(0, 10)
		queue.send(v)
		print('Send : {}'.format(v))

	MAX = 2
	worker = EventWorker(ThreadEventRunnerPool(MAX), SampleEventConsumer)
	def stop(signal, frame):
		print('EventWorker stopping...')
		worker.stop()
		return
	signal(SIGINT, stop)
	print('EventWorker running until break with keyboard interrupt...')
	worker.run()
	print('EventWorker stopped...')

	print('EventBroker clean...')
	con.deleteQueue('queue')
