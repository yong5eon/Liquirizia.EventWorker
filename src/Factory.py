# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)
from abc import ABCMeta, abstractmethod
from typing import Type, Union, Sequence

__all__ = (
	'Factory',
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
