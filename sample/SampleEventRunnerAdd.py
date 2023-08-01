# -*- coding: utf-8 -*-

from Liquirizia.EventRunner import EventRunner
from Liquirizia.EventBroker import EventBrokerHelper

__all__ = (
	'SampleEventRunnerAdd'
)


class SampleEventRunnerAdd(EventRunner):
	def __init__(self, event: str, headers: dict = None):
		self.event = event
		self.headers = headers
		return

	def run(self, body=None):
		res = body['a'] + body['b']
		print('{} + {} = {}'.format(
			body['a'],
			body['b'],
			res
		))
		if 'X-Reply-Broker' in self.headers.keys() and 'X-Reply-Broker-Queue' in self.headers.keys():
			EventBrokerHelper.Send(
				self.headers['X-Reply-Broker'], 
				queue=self.headers['X-Reply-Broker-Queue'], 
				event=self.type, 
				body=res, 
				format='text/plain', 
				charset='utf-8'
			)
		return

