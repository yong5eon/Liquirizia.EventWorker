# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Factory import Factory
from .EventRunner import (
	EventRunner,
	EventParameters,
	EventSetup,
	EventComplete,
	EventError,
)
from uuid import uuid4
from typing import Type, Sequence, Union, Any, Dict

__all__ = (
	'Context',
	'EventContext',
)


class Context(object):
	def __init__(
		self,
		factory: Type[Factory],
		runner: Type[EventRunner],
		properties: Any = None,
		setups: Union[EventSetup, Sequence[EventSetup]] = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		self.factory = factory
		self.runner = runner
		self.properties = properties
		self.setups = setups
		if self.setups and not isinstance(self.setups, Sequence):
			self.setups = [self.setups]
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		return


class EventContext(Singleton):
	"""Event Context Class"""
	def __init__(self):
		self.contexts = {}
		return

	def add(
		self,
		factory: Type[Factory],
		event: str,
		runner: Type[EventRunner],
		properties: Any = None,
		setups: Union[EventSetup, Sequence[EventSetup]] = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		if event in self.contexts.keys():
			raise RuntimeError('Event already exists')
		if setups and not isinstance(setups, Sequence):
			setups = [setups]
		if completes and not isinstance(completes, Sequence):
			completes = [completes]
		if errors and not isinstance(errors, Sequence):
			errors = [errors]
		self.contexts[event] = Context(
			factory=factory,
			runner=runner,
			properties=properties,
			setups=setups,
			completes=completes,
			errors=errors,
		)
		return
	
	def get(self, event: str) -> Context:
		return self.contexts.get(event, None)
	
	def events(self) -> Dict[str, Any]:
		return {k: v.properties for k, v in self.contexts.items()}
	