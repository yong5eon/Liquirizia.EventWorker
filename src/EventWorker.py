# -*- coding: utf-8 -*-

from .EventContext import EventContext
from .EventConsumer import EventConsumer
from .EventRunnerPool import EventRunnerPool

from .EventWorkerHandler import EventWorkerHandler

from Liquirizia.EventRunner import EventRunnerProperties, EventRunnerPropertiesHelper

from os.path import split
from pathlib import Path

__all__ = (
	'EventWorker'
)


class EventWorker(object):
	"""
	EventWorker
	"""
	def __init__(self, handler: EventWorkerHandler = None, count=1, size=0):
		"""
		constructor
		"""
		self.context = EventContext()
		self.handler = handler
		self.count = count
		self.size = size
		self.pool = None
		self.consumer = None
		return

	def run(self, concurrency=None):
		"""
		run as a worker
		"""
		try:
			if self.handler:
				self.handler.onInitialize(self.context.brokers(), self.count, self.size, concurrency)
			self.pool = EventRunnerPool(self.context, self.handler, size=concurrency)
			self.consumer = EventConsumer(self.context, self.pool, self.handler, self.count, self.size)
			if self.handler:
				self.handler.onStart()
			self.consumer.run()
			if self.handler:
				self.handler.onStop()
		except BaseException as e:
			if self.handler:
				self.handler.onError(e)
		return

	def stop(self):
		self.consumer.stop()
		self.pool.stop()
		return

	def add(self, properties: EventRunnerProperties):
		self.context.add(properties)
		return

	def load(self, path, name='properties', pattern=None):
		if not pattern:
			head, tail = split(path)
			ps = Path(head).glob(tail)
		else:
			ps = Path(path).rglob(pattern)
		for p in ps if ps else []:
			self.add(EventRunnerPropertiesHelper.Load(str(p), name))
		return
