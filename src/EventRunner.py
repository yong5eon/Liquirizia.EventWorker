# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any

__all__ = (
	'EventRunner',
	'EventComplete',
	'EventError',
)


class EventRunner(metaclass=ABCMeta):
	"""Event Runner Interface"""
	@abstractmethod
	def run(self, *args, **kwargs):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))


class EventComplete(metaclass=ABCMeta):
	"""Event Runner Complete Interface"""
	@abstractmethod
	def __call__(
		self,
		completion: Any,
		*args,
		**kwargs,
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class EventError(metaclass=ABCMeta):
	"""Event Runner Error Interface"""
	@abstractmethod
	def __call__(
		self,
		error: BaseException,
		*args,
		**kwargs,
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
