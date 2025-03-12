# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
)

from multiprocessing import get_context
from multiprocessing.pool import (
	Pool as PyProcessPool,
	ThreadPool as PyThreadPool,
)
from abc import ABC
from typing import Type, Union, Sequence, Mapping, Dict, Any

__all__ = (
	'EventRunnerFactory',
	'EventRunnerPool',
	'ThreadEventRunnerPool',
	'ProcessEventRunnerPool',
)


class EventRunnerFactory(object):
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
	def __call__(self, body: Any):
		try:
			runner = self.runner()
			if isinstance(body, Mapping):
				completion = runner.run(**body)
			elif isinstance(body, Sequence):
				completion = runner.run(*body)
			else:
				completion = runner.run(body)
		except Exception as e:
			for error in self.errors if self.errors else []:
				error(e)
		else:
			for complete in self.completes if self.completes else []:
				complete(completion)
			return


class EventRunnerPool(ABC):
	"""EventRunner Pool Abstract Class"""
	def __init__(self, pool: Union[PyProcessPool, PyThreadPool]):
		self.pool = pool
		self.runners = []
		return

	def __del__(self):
		self.stop()
		return

	def __len__(self):
		return len(self.runners)

	def add(
		self,
		runner: Type[EventRunner],
		body: Any,
		completes: Union[EventRunnerComplete, Sequence[EventRunnerComplete]] = None,
		errors: Union[EventRunnerError, Sequence[EventRunnerError]] = None
	):
		self.runners.append(self.pool.apply_async(
			EventRunnerFactory(runner, completes=completes, errors=errors),
			args=(body,),
			kwds={},
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
		self.pool = None
		return

	def shutdown(self):
		self.pool.terminate()
		self.pool.join()
		self.pool = None
		return


class ThreadEventRunnerPool(EventRunnerPool):
	"""EventRunner ThreadPool Class"""
	def __init__(self, max: int):
		super().__init__(PyThreadPool(max))
		return


class ProcessEventRunnerPool(EventRunnerPool):
	"""EventRunner ProcessPool Class"""
	def __init__(self, max: int):
		# super().__init__(get_context().Pool(max))
		super().__init__(pool=PyProcessPool(max))
		return	
