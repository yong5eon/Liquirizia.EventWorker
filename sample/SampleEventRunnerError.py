# -*- coding: utf-8 -*-

from Liquirizia.EventRunner import EventRunnerError

from Liquirizia.EventBroker import EventBrokerHelper

__all__ = (
	'SampleEventRunnerError'
)


class SampleEventRunnerError(EventRunnerError):
	def __init__(self, event):
		self.event = event
		return

	def __call__(self, event, headers=None, body=None, error=None):
		EventBrokerHelper.Send(
			'Sample',
			'queue.error',
			event=self.event,
			body={
				'event': event,
				'headers': headers,
				'body': body,
				'error': str(error) if error else None
			}
		)
		return
