# -*- coding: utf-8 -*-

from Liquirizia.EventRunner import EventRunnerProperties
from Liquirizia.EventRunner.Types import EventWorker
from Liquirizia.EventRunner.Errors import NotSupportedTypeError

__all__ = (
	'EventContext'
)


class EventContext(object):
	"""
	Event Context Class
	"""
	def __init__(self):
		self.context = {}
		self.ps = {}
		return

	def add(self, properties: EventRunnerProperties):
		if not isinstance(properties.type, EventWorker):
			raise NotSupportedTypeError(properties.type.__class__.__name__)
		if properties.type.name not in self.context:
			self.context[properties.type.name] = set()
		self.context[properties.type.name].add(properties.type.queue)
		if (properties.type.name, properties.type.queue) not in self.ps:
			self.ps[(properties.type.name, properties.type.queue)] = []
		self.ps[(properties.type.name, properties.type.queue)].append(properties)
		return

	def brokers(self):
		return self.context

	def match(self, broker: str, key: str):
		if (broker, key) not in self.ps:
			return None
		return self.ps[(broker, key)]
