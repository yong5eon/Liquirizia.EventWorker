# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)
from .Factory import Factory

from typing import Type, Sequence, Union, Any, List, Dict

__all__ = (
	'EventContext',
	'EventRunnerFactory',
)

class EventRunnerFactory(Factory):
	def __init__(
		self,
		runner: Type[EventRunner],
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None,
	):
		self.runner = runner
		self.completes = completes
		if self.completes and not isinstance(self.completes, Sequence):
			self.completes = [self.completes]
		self.errors = errors
		if self.errors and not isinstance(self.errors, Sequence):
			self.errors = [self.errors]
		return
	def __call__(self, *args, **kwargs):
		try:
			runner = self.runner()
			completion = runner.run(*args, **kwargs)
		except Exception as e:
			for error in self.errors if self.errors else []:
				error(e)
		else:
			for complete in self.completes if self.completes else []:
				complete(completion)
			return


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
		factory: Type[Factory] = EventRunnerFactory,
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
		return self.context.keys()
	
	def parameters(self) -> Dict[str, Any]:
		return {k: v['parameters'] for k, v in self.context.items()}
	
	def parameter(self, event: str) -> Any:
		return self.context[event]['parameters']

