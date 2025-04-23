# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Factory import Factory
from .EventRunner import (
	EventRunner,
	EventParameters,
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
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		self.factory = factory
		self.runner = runner
		self.properties = properties
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
		self.tasks = {} 
		return

	def add(
		self,
		factory: Type[Factory],
		event: str,
		runner: Type[EventRunner],
		properties: Any = None,
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
	):
		if event in self.contexts.keys():
			raise RuntimeError('Event already exists')
		if completes and not isinstance(completes, Sequence):
			completes = [completes]
		if errors and not isinstance(errors, Sequence):
			errors = [errors]
		self.contexts[event] = Context(
			factory=factory,
			runner=runner,
			properties=properties,
			completes=completes,
			errors=errors,
		)
		return
	
	def get(self, event: str) -> Context:
		return self.contexts.get(event, None)
	
	def events(self) -> Dict[str, Any]:
		return {k: v.properties for k, v in self.contexts.items()}
	
	def attach(self, event: str, parameters: EventParameters, id: str = None):
		if not id: id = uuid4().hex
		self.tasks[id] = {
			'event': event,
			'parameters': {
				'args': parameters.args,
				'kwargs': parameters.kwargs,
			}
		}
		return id

	def detach(self, id: str):
		if id in self.tasks: del self.tasks[id]
		return

	def status(self):
		return {
			'events': self.events(),
			'concurrency': len(self.tasks.items()),
			'tasks': self.tasks,
		}
