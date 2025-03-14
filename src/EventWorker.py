# -*- coding: utf-8 -*-

from .EventRunnerPool import EventRunnerPool
from .EventInvoker import EventInvoker

from typing import Type

__all__ = (
	'Event',
	'EventWorker'
)


class EventWorker(object):
	"""Event Worker"""
	def __init__(self, pool: EventRunnerPool, invoker: Type[EventInvoker]):
		self.pool = pool
		self.invoker = invoker(pool)
		return

	def run(self):
		self.invoker.run()
		return

	def stop(self):
		self.invoker.stop()
		return
