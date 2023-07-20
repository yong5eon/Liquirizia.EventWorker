# -*- coding: utf-8 -*-

from Liquirizia.EventRunner import EventRunner

__all__ = (
	'SampleEventRunnerSub'
)


class SampleEventRunnerSub(EventRunner):
	def __init__(self, event: str, headers: dict = None):
		self.event = event
		self.headers = headers
		return

	def run(self, body=None):
		print('{} - {} = {}'.format(
			body['a'],
			body['b'],
			body['a'] - body['b']
		))
		return body['a'] - body['b']
