# -*- coding: utf-8 -*-

from multiprocessing import get_context

__all__ = (
	'EventWorkerContext'
)


class EventWorkerContext(object):
	def __init__(self):
		self.event = get_context().Manager().Event()
		return
	def stop(self):
		self.event.set()
		return
	def __bool__(self):
		return not bool(self.event.is_set())

