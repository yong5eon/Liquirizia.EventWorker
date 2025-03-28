# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventComplete,
	EventError,
)
from .Factory import Factory
from .Context import (
	Context,
	EventFactory,
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


class Parameters(object):
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		return


class Pool(ABC):
	"""EventRunner Pool Abstract Class"""
	def __init__(self, pool: Union[PyProcessPool, PyThreadPool]):
		self.pool = pool
		self.runners = []
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
	
	def run(self, event: str, parameters: Parameters = Parameters()):
		ctx = Context()
		props = ctx.context.get(event, None)
		if not event:
			raise RuntimeError('Event not found')
		self.add(
			event,
			props['runner'],
			completes=props['completes'],
			errors=props['errors'],
			parameters=parameters,
			factory=props['factory'],
		)
		return

	def add(
		self,
		event: str,
		runner: Type[EventRunner],
		completes: Union[EventComplete, Sequence[EventComplete]] = None,
		errors: Union[EventError, Sequence[EventError]] = None,
		parameters: Parameters = Parameters(),
		factory: Type[Factory] = EventFactory,
	):
		self.runners.append(self.pool.apply_async(
			factory(event, runner, completes=completes, errors=errors),
			args=parameters.args,
			kwds=parameters.kwargs,
			error_callback=None
		))
		return
	
	def waits(self, timeout=None):
		for runner in self.runners:
			runner.wait(timeout)
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
