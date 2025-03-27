# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .EventRunner import (
	EventRunner,
	EventComplete,
	EventError,
)
from .Factory import Factory

from uuid import uuid4
from os import getpid
from threading import get_ident
from typing import Type, Sequence, Union, Any, List, Dict

__all__ = (
	'Context',
	'EventFactory',
)

class Parameters(object):
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		return


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
		ctx = Context()
		try:
			id = '{}.{}'.format(getpid(), get_ident())
			ctx.attach(self.event, Parameters(*args, **kwargs), id)
			runner = self.runner()
			completion = runner.run(*args, **kwargs)
		except Exception as e:
			for error in self.errors if self.errors else []:
				error(e, *args, **kwargs)
		else:
			for complete in self.completes if self.completes else []:
				complete(completion, *args, **kwargs)
		finally:
			ctx.detach(id)
			return


class Context(Singleton):
	"""Event Context Class"""
	def __init__(self):
		self.context = {}
		self.concurrent = {} 
		return

	def add(
		self,
		event: str,
		runner: Type[EventRunner],
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
		factory: Type[Factory] = EventFactory,
		eventParameters: Any = None,
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
			'factory': factory,
			'parameters': eventParameters,
		}
		return
	
	def events(self) -> List[str]:
		return [k for k in self.context.keys()]
	
	def parameters(self) -> Dict[str, Any]:
		return {k: v['parameters'] for k, v in self.context.items()}
	
	def parameter(self, event: str) -> Any:
		return self.context[event]['parameters']
	
	def attach(self, event: str, parameters: Parameters, id: str = None):
		if not id: id = uuid4().hex
		self.concurrent[id] = {
			'event': event,
			'parameters': {
				'args': parameters.args,
				'kwargs': parameters.kwargs,
			}
		}
		return id

	def detach(self, id: str):
		if id in self.concurrent:
			del self.concurrent[id]
		return

	def status(self):
		return {
			'events': {k: v['parameters'] for k, v in self.context.items()},
			'concurrency': len(self.concurrent.items()),
			'tasks': {k: {
				'event': v['event'],
				'args': v['parameters']['args'],
				'kwargs': v['parameters']['kwargs'],
			} for k, v in self.concurrent.items()},
		}
