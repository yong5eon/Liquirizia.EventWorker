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
	ApplyResult,
)
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Union, Sequence, Mapping, Dict, Any
from threading import Lock

__all__ = (
	'Parameters',
	'Pool',
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
		# We'll capture this in callbacks; it will be set right after apply_async returns
		tid = None

		def cleanup(_: Any = None):
			# Remove the task from runners when done or errored
			if tid is None:
				return
			with self.lock:
				self.runners.pop(tid, None)
			return

		task: ApplyResult = self.pool.apply_async(
			context.factory(event, context.runner, completes=context.completes, errors=context.errors),
			args=parameters.args,
			kwds=parameters.kwargs,
			callback=cleanup,  # on success
			error_callback=cleanup,  # on error
		)
		# Assign the tid after ApplyResult is created; callbacks will see the updated value
		tid = id(task)
		with self.lock:
			self.runners[tid] = task
		return tid
	
	def waits(self, timeout=None):
		# Iterate over a snapshot to avoid dict-size-change errors from callbacks
		for task in list(self.runners.values()):
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
		return self.max
	
	def count(self):
		# Remove completed tasks from self.runners
		with self.lock:
			completed = [tid for tid, task in self.runners.items() if task.ready()]
			for tid in completed:
				del self.runners[tid]
			return len(self.runners)


class ThreadPool(Pool):
	"""EventRunner ThreadPool Class"""
	def __init__(self, max: int = None):
		super().__init__(PyThreadPool(max), max=max)
		return


class ProcessPool(Pool):
	"""EventRunner ProcessPool Class"""
	def __init__(self, max: int = None):
		super().__init__(pool=PyProcessPool(max), max=max)
		return	
