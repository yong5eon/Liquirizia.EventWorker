# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventParameters,
	EventComplete,
	EventError,
)
from .EventContext import (
	EventContext,
	Context,
)

from multiprocessing import get_context
from multiprocessing.pool import (
	Pool as PyProcessPool,
	ThreadPool as PyThreadPool,
)
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Union, Sequence, Mapping, Dict, Any

__all__ = (
	'Parameters',
	'Pool',
	'ThreadPool',
	'ProcessPool',
)


class Pool(ABC):
	"""EventRunner Pool Abstract Class"""
	def __init__(self, pool: Union[PyProcessPool, PyThreadPool]):
		self.pool = pool
		self.runners = {}
		return

	def __del__(self):
		try:
			self.stop()
		except:
			pass
		finally:
			try:
				self.pool = None
			except:
				pass
		return

	def __len__(self):
		return len(self.runners)
	
	def run(
		self,
		event: str,
		parameters: EventParameters = EventParameters(),
	):
		ec = EventContext()
		context: Context = ec.get(event)
		if not context:
			return
		task = self.pool.apply_async(
			context.factory(event, context.runner, completes=context.completes, errors=context.errors),
			args=parameters.args,
			kwds=parameters.kwargs,
			error_callback=None
		)
		self.runners[id(task)] = task
		return id(task)
	
	def waits(self, timeout=None):
		for id, task in self.runners.items():
			task.wait(timeout)
		return

	def stop(self):
		self.pool.close()
		self.pool.join()
		return

	def shutdown(self):
		self.pool.terminate()
		self.pool.join()
		return


class ThreadPool(Pool):
	"""EventRunner ThreadPool Class"""
	def __init__(self, max: int = None):
		super().__init__(PyThreadPool(max))
		return


class ProcessPool(Pool):
	"""EventRunner ProcessPool Class"""
	def __init__(self, max: int = None):
		super().__init__(pool=PyProcessPool(max))
		return	
