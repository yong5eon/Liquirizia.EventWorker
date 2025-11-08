# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventParameters,
	EventSetup,
	EventComplete,
	EventError,
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
		event: str,
		runner: Type[EventRunner],
		setups: Union[EventSetup, Sequence[EventSetup]] = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	@abstractmethod
	def __call__(self, *args, **kwargs):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
