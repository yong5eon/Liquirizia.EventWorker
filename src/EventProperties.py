# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)
from .EventContext import EventContext

from typing import Type, Sequence, Union

__all__ = (
	'EventProperties',
)


class EventProperties(object):
	"""Event Properties Decorator"""
	def __init__(
		self,
		event: str,
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None,
	):
		self.event = event
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		return

	def __call__(self, o: Type[EventRunner]):
		ctx = EventContext()
		ctx.add(
			event=self.event,
			runner=o,
			completes=self.completes,
			errors=self.errors,
		)
		return o
