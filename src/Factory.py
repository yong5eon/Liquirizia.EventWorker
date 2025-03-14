# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)
from abc import ABCMeta, abstractmethod
from typing import Type, Union, Sequence, Any

__all__ = (
	'Factory',
	'EventRunnerFactory',
)


class Factory(metaclass=ABCMeta):
	@abstractmethod
	def __init__(
		self,
		runner: Type[EventRunner],
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None,
	):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	@abstractmethod
	def __call__(self, *args, **kwargs):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class EventRunnerFactory(Factory):
	def __init__(
		self,
		runner: Type[EventRunner],
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None,
	):
		self.runner = runner
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		return
	def __call__(self, *args, **kwargs):
		try:
			runner = self.runner()
			completion = runner.run(*args, **kwargs)
		except Exception as e:
			for error in self.errors if self.errors else []:
				error(e)
		else:
			for complete in self.completes if self.completes else []:
				complete(completion)
			return
