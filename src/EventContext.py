# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)

from typing import Type, Sequence, Union

__all__ = (
	'EventContext',
)


class EventContext(Singleton):
	"""Event Context Class"""
	def __init__(self):
		self.context = {}
		return

	def add(
		self,
		event: str,
		runner: Type[EventRunner],
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None,
	):
		if event in self.context:
			raise RuntimeError('Event already exists')
		if completes and not isinstance(completes, Sequence):
			completes = [completes]
		if errors and not isinstance(errors, Sequence):
			errors = [errors]
		self.context[event] = {
			'runner': runner,
			'completes': completes,
			'errors': errors,
		}
		return

