# -*- coding: utf-8 -*-

from .Factory import Factory
from .EventRunner import (
	EventRunner,
	EventComplete,
	EventError,
)
from .Context import (
	Context,
	EventFactory,
)

from typing import Type, Sequence, Union, Any

__all__ = (
	'EventProperties',
)


class EventProperties(object):
	"""Event Properties Decorator"""
	def __init__(
		self,
		event: str,
		parameters: Any = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
		factory: Type[Factory] = EventFactory,
	):
		self.event = event
		self.parameters = parameters
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		self.factory = factory
		return

	def __call__(self, o: Type[EventRunner]):
		ctx = Context()
		ctx.add(
			event=self.event,
			runner=o,
			completes=self.completes,
			errors=self.errors,
			factory=self.factory,
			eventParameters=self.parameters,
		)
		return o
