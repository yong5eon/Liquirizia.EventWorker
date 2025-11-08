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
	'Status',
)


class Status(Singleton):
	"""Status Class"""
	def __init__(self, tasks: Dict = None):
		self.tasks = tasks if tasks is not None else {}
		return
	
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

	def stats(self):
		return {
			'concurrency': len(self.tasks.items()),
			'tasks': self.tasks.copy(),
		}
