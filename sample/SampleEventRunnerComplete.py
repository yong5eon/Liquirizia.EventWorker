# -*- coding: utf-8 -*-

from Liquirizia.EventRunner import EventRunnerComplete

from Liquirizia.EventBroker import EventBrokerHelper

__all__ = (
	'SampleEventRunnerComplete'
)


class SampleEventRunnerComplete(EventRunnerComplete):
	def __init__(self, event):
		self.event = event
		return

	def __call__(self, event, headers=None, body=None, res=None):
		EventBrokerHelper.Send(
			'Sample',
			'queue.complete',
			event=self.event,
			body={
				'event': event,
				'headers': headers,
				'body': body,
				'res': res
			}
		)
		return
