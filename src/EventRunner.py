# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any

__all__ = (
	'EventRunner',
	'EventRunnerComplete',
	'EventRunnerError',
)


class EventRunner(metaclass=ABCMeta):
	"""Event Runner Interface"""
	@abstractmethod
	def run(self, *args, **kwargs):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))


class EventRunnerComplete(metaclass=ABCMeta):
	"""Event Runner Complete Interface"""
	@abstractmethod
	def __call__(
		self,
		completion: Any
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class EventRunnerError(metaclass=ABCMeta):
	"""Event Runner Error Interface"""
	@abstractmethod
	def __call__(
		self,
		error: BaseException,
	):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
