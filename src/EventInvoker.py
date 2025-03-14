# -*- coding: utf-8 -*-

from .EventRunnerPool import EventRunnerPool

from abc import ABCMeta, abstractmethod

__all__ = (
	'EventInvoker',
)


class EventInvoker(metaclass=ABCMeta):
	"""Event Invoker Interface"""
	@abstractmethod
	def __init__(self, pool: EventRunnerPool):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	@abstractmethod
	def run(self):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
	@abstractmethod
	def stop(self):
		raise NotImplementedError('{} must be implemented stop'.format(self.__class__.__name__))
