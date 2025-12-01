# -*- coding: utf-8 -*-

from .EventRunner import (
	EventRunner,
	EventParameters,
	EventSetup,
	EventComplete,
	EventError,
)
from .EventContext import (
	EventContext,
	Context,
)
from .Status import Status

from multiprocessing import Manager, get_start_method
from multiprocessing.pool import (
	Pool as PyProcessPool,
	ThreadPool as PyThreadPool,
	ApplyResult,
)
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Union, Sequence, Mapping, Dict, Any
from threading import Lock

__all__ = (
	'Parameters',
	'Pool',
	'Setup',
	'ThreadPool',
	'ProcessPool',
)


class Pool(ABC):
	"""EventRunner Pool Abstract Class"""
	def __init__(self, pool: Union[PyProcessPool, PyThreadPool], max: int = None):
		self.pool = pool
		self.runners = {}
		self.max = max
		self.lock = Lock()
		self.counter = 0  # monotonically increasing task id
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

	def run(
		self,
		event: str,
		parameters: EventParameters = EventParameters(),
	):
		ec = EventContext()
		context: Context = ec.get(event)
		if not context:
			return
		# Pre-allocate a unique id to eliminate race between ultra-fast task completion and id assignment
		with self.lock:
			self.counter += 1
			tid = self.counter
			# Placeholder before async starts (filled with ApplyResult below)
			self.runners[tid] = None

		def cleanup(_: Any = None):
			# Remove metadata when done (success or error)
			with self.lock:
				self.runners.pop(tid, None)
			return

		task: ApplyResult = self.pool.apply_async(
			context.factory(event, context.runner, setups=context.setups, completes=context.completes, errors=context.errors),
			args=parameters.args,
			kwds=parameters.kwargs,
			callback=cleanup,  # on success
			error_callback=cleanup,  # on error
		)
		# Fill in the actual task object if it hasn't already been cleaned up by an extremely fast completion
		with self.lock:
			if tid in self.runners:
				self.runners[tid] = task
		return tid
	
	def waits(self, timeout=None):
		# Iterate over a snapshot to avoid dict-size-change errors from callbacks
		for task in list(self.runners.values()):
			if task is not None:
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

	def size(self):
		"""
		Returns the maximum pool size.

		Returns:
			int or None: The maximum number of concurrent tasks allowed in the pool,
			or None if no maximum was specified.
		"""
		return self.max
	
	def count(self):
		"""
		Returns the number of currently running tasks.
		"""
		with self.lock:
			return sum(1 for task in self.runners.values() if task is not None)


class Setup(metaclass=ABCMeta):
	"""EventRunner Pool Setup Interface"""
	@abstractmethod
	def __call__(self):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class ThreadPoolSetup(Setup):
	"""EventRunner ThreadPoolSetup Class"""
	def __init__(
		self,
		setups: Union[Setup, Sequence[Setup]],
	):
		self.setups = setups
		if self.setups and not isinstance(self.setups, Sequence):
			self.setups = [self.setups]
		return

	def __call__(self):
		for setup in self.setups if self.setups else []: setup()
		return


class ThreadPool(Pool):
	"""EventRunner ThreadPool Class"""
	def __init__(self, max: int = None, setups: Union[Setup, Sequence[Setup]] = None):
		self.tasks = Manager().dict()
		self.status = Status(tasks=self.tasks)
		super().__init__(PyThreadPool(max, initializer=ThreadPoolSetup(setups)), max=max)
		return


class SpawnProcessPoolSetup(Setup):
	"""EventRunner ProcessPool Setup Class for Spawn"""
	def __init__(
		self,
		setups: Union[Setup, Sequence[Setup]],
		tasks: Any,
	):
		self.setups = setups
		if self.setups and not isinstance(self.setups, Sequence):
			self.setups = [self.setups]
		self.tasks = tasks
		return

	def __call__(self):
		self.status = Status(tasks=self.tasks)
		for setup in self.setups if self.setups else []: setup()
		return


class ForkProcessPoolSetup(Setup):
	"""EventRunner ProcessPoolSetup Class for Fork"""
	def __init__(
		self,
		setups: Union[Setup, Sequence[Setup]],
	):
		self.setups = setups
		if self.setups and not isinstance(self.setups, Sequence):
			self.setups = [self.setups]
		return

	def __call__(self):
		for setup in self.setups if self.setups else []: setup()
		return


class ProcessPool(Pool):
	"""EventRunner ProcessPool Class"""
	def __init__(self, max: int = None, setups: Union[Setup, Sequence[Setup]] = None):
		self.tasks = Manager().dict()
		self.status = Status(tasks=self.tasks)
		if get_start_method() in ('spawn', 'forkserver'):
			super().__init__(PyProcessPool(max, initializer=SpawnProcessPoolSetup(setups, tasks=self.tasks)), max=max)
		else:
			super().__init__(PyProcessPool(max, initializer=ForkProcessPoolSetup(setups)), max=max)
		return
