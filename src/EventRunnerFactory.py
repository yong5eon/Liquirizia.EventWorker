# -*- coding: utf-8 -*-

from Liquirizia.Parallelizer import Runnable
from Liquirizia.EventBroker import EventBrokerHelper
from Liquirizia.EventRunner import EventRunnerProperties
from Liquirizia.EventRunner.Errors import *

from .EventWorkerHandler import EventWorkerHandler

__all__ = (
	'EventRunnerFactory'
)


class EventRunnerFactory(Runnable):
	def __init__(self, handler: EventWorkerHandler, properties: EventRunnerProperties, broker: str, event: str, headers: dict = None, body=None):
		self.handler = handler
		self.properties = properties
		self.broker = broker
		self.event = event
		self.headers = headers
		self.body = body
		return

	def run(self):
		try:
			if self.handler:
				self.handler.onEvent(self.event, self.headers, self.body)
			if self.event != self.properties.type.event:
				raise NotSupportedEventError(self.event)
			if self.properties.header:
				self.headers = self.properties.header(self.headers)
			if self.properties.body:
				self.body = self.properties.body(self.body)
			obj = self.properties.object(self.event, self.headers)
			obj.run(self.body)
			for callback in self.properties.completes if self.properties.completes else []:
				callback(self.event, self.headers, self.body)
			if self.handler:
				self.handler.onEventSuccess(self.event, self.headers, self.body)
		except BaseException as e:
			for callback in self.properties.errors if self.properties.errors else []:
				callback(self.event, self.headers, self.body, e)
			if self.handler:
				self.handler.onEventError(self.event, self.headers, self.body, e)
		return
