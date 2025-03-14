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

from Liquirizia.EventBroker import Helper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
	Consumer,
	Queue,
	EventHandler,
) 

from SampleEventRunner import *

from Liquirizia.Logger import (
	LOG_INIT,
	LOG_LEVEL_DEBUG,
	LOG_INFO,
)

from signal import signal, SIGINT
from random import randint


class SampleEventHandler(EventHandler):
	def __init__(self, pool: EventRunnerPool):
		self.pool = pool
		return
	def __call__(self, event):
		LOG_INFO('Event : type={}, {}'.format(event.type, event.body))
		self.pool.run(
			event=event.type,
			parameters=EventParameters(**event.body)
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
		LOG_INFO('Consumer running...')
		self.consumer.run()
		LOG_INFO('Consumer stopped...')
		return
	def stop(self):
		if self.consumer:
			self.consumer.stop()
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

	LOG_INFO('EventBroker init...')
	EVENT = ['+', '-', '*', '/', '%']
	con: Connection = Helper.Get('Sample')
	con.createQueue('queue')
	queue: Queue = con.queue('queue')
	for i in range(100):
		event = EVENT[randint(0, 4)]
		a = randint(0, 9)
		b = randint(0, 9)
		queue.send({'a': a, 'b': b}, event=event)

	worker = EventWorker(ThreadEventRunnerPool(), SampleEventConsumer)
	def stop(signal, frame):
		LOG_INFO('EventWorker stopping...')
		worker.stop()
		return
	signal(SIGINT, stop)
	LOG_INFO('EventWorker running until break with keyboard interrupt...')
	worker.run()
	LOG_INFO('EventWorker stopped...')

	LOG_INFO('EventBroker clean...')
	con.deleteQueue('queue')
