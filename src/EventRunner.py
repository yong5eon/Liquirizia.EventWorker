# -*- coding: utf-8 -*-

from abc import ABC, ABCMeta, abstractmethod
from typing import Any

__all__ = (
	'EventRunner',
	'EventParameters',
	'EventInit',
	'EventComplete',
	'EventError',
)


class EventParameters(object):
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		return
	def __repr__(self):
		return '{}({})'.format(
			self.__class__.__name__,
			', '.join([str(arg) for arg in self.args] + ['{}={}'.format(k, v) for k, v in self.kwargs.items()])
		)

class EventRunner(ABC):
	"""Event Runner Interface"""
	def __init__(self, *args): pass
	@abstractmethod
	def run(self, **kwargs):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
	

class EventSetup(metaclass=ABCMeta):
	"""Event Runner Setup Interface"""
	@abstractmethod
	def __call__(self, parameters: EventParameters):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class EventComplete(metaclass=ABCMeta):
	"""Event Runner Complete Interface"""
	@abstractmethod
	def __call__(
		self,
		parameters: EventParameters,
		completion: Any,
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class EventError(metaclass=ABCMeta):
	"""Event Runner Error Interface"""
	@abstractmethod
	def __call__(
		self,
		parameters: EventParameters,
		error: BaseException,
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
