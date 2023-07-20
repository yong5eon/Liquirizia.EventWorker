# -*- coding: utf-8 -*-

from Liquirizia.Validator import Error

from Liquirizia.EventRunner.Errors import InvalidBodyError

__all__ = (
	'SampleErrorFactory'
)


class SampleErrorFactory(Error):
	def __init__(self, reason):
		self.reason = reason
		return

	def __call__(self, parameters, *args, **kwargs):
		return InvalidBodyError(self.reason)
