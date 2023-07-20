# -*- coding: utf-8 -*-

from Liquirizia.Parallelizer import Handler
from Liquirizia.Parallelizer.MultiThread import Pool

from .EventWorkerHandler import EventWorkerHandler
from .EventContext import EventContext
from .EventRunnerFactory import EventRunnerFactory

from .EventRunnerOptions import EventRunnerOptions

__all__ = (
	'EventRunnerPool'
)


class EventRunnerPool(Pool, Handler):
	def __init__(self, context: EventContext, handler: EventWorkerHandler = None, size: int = None):
		super(EventRunnerPool, self).__init__(size, self)
		self.eventWorkerHandler = handler
		self.context = context
		return

	def onInitialize(self, *args, **kwargs):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onInitializeRunner(
				args[2],
				args[3],
				args[4],
				args[5],
			)
		return

	def onStart(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onStartRunner()
		return

	def onCompleted(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onCompleteRunner()
		return

	def onStopped(self):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onStopRunner()
		return

	def onError(self, error=None):
		if self.eventWorkerHandler:
			self.eventWorkerHandler.onErrorRunner(error)
		return

	def add(self, broker: str, key: str, type: str, headers: dict = None, body = None, opts: EventRunnerOptions = None):
		ps = self.context.match(broker, key)
		for properties in ps if ps else []:
			super(EventRunnerPool, self).add(
				EventRunnerFactory,
				self.eventWorkerHandler,
				properties,
				broker,
				type,
				headers,
				body,
				opts,
			)
		return
