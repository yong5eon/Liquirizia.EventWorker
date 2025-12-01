# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton


from .EventRunner import (
	EventParameters,
)
from uuid import uuid4
from typing import Dict

__all__ = (
	'Status',
)


class Status(Singleton):
	"""Status Class"""
	def __init__(self, tasks: Dict):
		self.tasks = tasks
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
			'concurrency': len(self.tasks),
			'tasks': self.tasks.copy(),
		}
