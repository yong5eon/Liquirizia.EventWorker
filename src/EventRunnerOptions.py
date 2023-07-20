# -*- coding: utf-8 -*-

__all__ = (
	'EventRunnerOptions',
)


class EventRunnerOptions(object):
	"""
	Event Runner Options Class
	"""
	def __init__(
		self,
		reply: str = None,
	):
		self.__options__ = {
			'reply': reply,
		}
		return

	@property
	def reply(self):
		return self.__options__['reply']
