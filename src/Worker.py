# -*- coding: utf-8 -*-

from .Pool import Pool
from .Invoker import Invoker
from .Utils import Loader

from typing import Type

__all__ = (
	'Worker'
)


class Worker(object):
	"""Event Worker"""
	def __init__(self, pool: Pool, invoker: Type[Invoker]):
		self.pool = pool
		self.invoker = invoker(pool)
		return

	def run(self):
		self.invoker.run()
		return

	def stop(self):
		self.invoker.stop()
		return
	
	def load(self, mod: str = None, path: str = None, ext: str = 'py'):
		"""Load module"""
		load = Loader()
		return load(mod=mod, path=path, ext=ext)
