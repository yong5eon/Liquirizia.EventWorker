# -*- coding: utf-8 -*-

from .Factory import Factory
from .EventRunner import (
	EventRunner,
	EventParameters,
	EventComplete,
	EventError,
)
from .EventContext import EventContext

from os import getpid
from threading import get_ident
from typing import Type, Sequence, Union, Any

__all__ = (
	'EventFactory',
	'EventProperties',
)


class EventFactory(Factory):
	def __init__(
		self,
		event: str,
		runner: Type[EventRunner],
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		self.event = event
		self.runner = runner
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		return
	def __call__(self, *args, **kwargs):
		ctx = EventContext()
		try:
			id = '{}.{}'.format(getpid(), get_ident())
			ctx.attach(self.event, EventParameters(*args, **kwargs), id)
			runner = self.runner(*args) if args else self.runner()
			completion = runner.run(**kwargs) if kwargs else runner.run()
		except Exception as e:
			for error in self.errors if self.errors else []:
				error(EventParameters(*args, **kwargs), e)
		else:
			for complete in self.completes if self.completes else []:
				complete(EventParameters(*args, **kwargs), completion)
		finally:
			ctx.detach(id)
			return


class EventProperties(object):
	"""Event Properties Decorator"""
	def __init__(
		self,
		event: str,
		properties: Any = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
		factory: Type[Factory] = EventFactory,
	):
		self.event = event
		self.properties = properties
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		self.factory = factory
		return

	def __call__(self, o: Type[EventRunner]):
		ctx = EventContext()
		ctx.add(
			factory=self.factory,
			event=self.event,
			runner=o,
			properties=self.properties,
			completes=self.completes,
			errors=self.errors,
		)
		return o
