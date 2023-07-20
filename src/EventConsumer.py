# -*- coding: utf-8 -*-

from Liquirizia.Parallelizer import Handler
from Liquirizia.Parallelizer.MultiThread import Runner

from .EventWorkerHandler import EventWorkerHandler
from .EventRunnerPool import EventRunnerPool
from .EventContext import EventContext
from .Consumer import Consumer

__all__ = (
	'EventConsumer'
)


class EventConsumer(Runner, Handler):
	def __init__(self, context: EventContext, pool: EventRunnerPool, handler: EventWorkerHandler = None, count: int = 1, size: int = 0):
		super(EventConsumer, self).__init__(self)
		self.eventWorkerHandler = handler
		self.context = context
		self.pool = pool
		self.count = count
		self.size = size
		return

	def onInitialize(self, *args, **kwargs):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onInitializeConsumer(args[1], args[2], args[3], args[4])
		return

	def onStart(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onStartConsumer()
		return

	def onCompleted(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onStopConsumer()
		return

	def onStopped(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onStopConsumer()
		return

	def onError(self, error=None):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onErrorConsumer(error)
		return

	def run(self):
		for broker, queues in self.context.brokers().items():
			self.add(Consumer, self.pool, broker, queues, self.count, self.size)
		super(EventConsumer, self).run()
		return
