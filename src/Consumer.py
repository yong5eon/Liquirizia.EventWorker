# -*- coding: utf-8 -*-

from Liquirizia.Parallelizer import Runnable
from Liquirizia.EventBroker import EventBrokerHelper, Callback, Event

from .EventRunnerPool import EventRunnerPool
from .EventRunnerOptions import EventRunnerOptions

__all__ = (
	'Consumer'
)


class Consumer(Runnable, Callback):
	def __init__(self, pool: EventRunnerPool, broker: str, queues: list[str], count: int = 1, size: int = 0):
		self.pool = pool
		self.broker = broker
		self.queues = queues
		self.count = count
		self.size = size
		return

	def __call__(self, event: Event):
		try:
			self.pool.add(
				self.broker,
				event.key,
				event.type,
				event.headers(),
				event.body,
				EventRunnerOptions(
					reply=event.reply
				)
			)
			event.ack()
		except BaseException:
			event.nack()
		return

	def run(self):
		broker = EventBrokerHelper.Get(self.broker)
		consumer = broker.consumer(callback=self)
		consumer.qos(self.count, self.size)
		for queue in self.queues:
			consumer.consume(queue)
		consumer.run()
		return
