# -*- coding: utf-8 -*-

from .Pool import Pool

from abc import ABCMeta, abstractmethod

__all__ = (
	'Invoker',
)


class Invoker(metaclass=ABCMeta):
	"""Event Invoker Interface"""
	@abstractmethod
	def __init__(self, pool: Pool):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))
	@abstractmethod
	def run(self):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
	@abstractmethod
	def stop(self):
		raise NotImplementedError('{} must be implemented stop'.format(self.__class__.__name__))
