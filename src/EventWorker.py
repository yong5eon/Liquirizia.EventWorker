# -*- coding: utf-8 -*-

from .EventRunnerPool import EventRunnerPool
from .EventInvoker import EventInvoker
from .EventWorkerContext import EventWorkerContext

from typing import Type

__all__ = (
	'Event',
	'EventWorker'
)


class EventWorker(object):
	"""Event Worker"""
	def __init__(self, pool: EventRunnerPool, invoker: Type[EventInvoker]):
		self.context = EventWorkerContext()
		self.invoker = invoker(self.context, pool)
		self.pool = pool
		return

	def run(self):
		self.invoker.run()
		return

	def stop(self):
		self.invoker.stop()
		self.context.stop()
		return
