# -*- coding: utf-8 -*-

from Liquirizia.Logger import LOG_INITIALIZE, LOG_LEVEL_DEBUG, LOG_INFO, LOG_ERROR, LOG_EXCEPTION, LOG_DEBUG

from Liquirizia.EventWorker import EventWorkerHandler

__all__ = (
	'SampleEventWorkerHandler'
)


class SampleEventWorkerHandler(EventWorkerHandler):
	def onInitialize(self, brokers, count, size, concurrency):
		LOG_INITIALIZE(LOG_LEVEL_DEBUG, name='EVENT_WORKER')
		LOG_INFO('EVENT WORKER INIT     : {}, {}, {}'.format(count, size, concurrency))
		return

	def onStart(self):
		LOG_INFO('EVENT WORKER START')
		return

	def onStop(self):
		LOG_INFO('EVENT WORKER STOP')
		return

	def onError(self, error=None):
		LOG_ERROR('EVENT WORKER ERROR    :')
		LOG_EXCEPTION(LOG_LEVEL_DEBUG, error)
		return

	def onInitializeConsumer(self, broker, queues, count, size):
		LOG_INFO('EVENT CONSUMER INIT   : {}, {}, {}'.format(broker, count, size))
		for queue in queues:
			LOG_DEBUG('QUEUE                 : {}'.format(queue))
		return

	def onStartConsumer(self):
		LOG_INFO('EVENT CONSUMER START')
		return

	def onStopConsumer(self):
		LOG_INFO('EVENT CONSUMER STOP')
		return

	def onErrorConsumer(self, error=None):
		LOG_ERROR('EVENT CONSUMER ERROR :')
		LOG_EXCEPTION(LOG_LEVEL_DEBUG, error)
		return

	def onInitializeRunner(self, broker, event, headers=None, body=None):
		LOG_INFO('EVENT RUNNER INIT     : {}, {}, {}, {}'.format(
			broker,
			event,
			headers,
			body,
		))
		return

	def onStartRunner(self):
		LOG_INFO('EVENT RUNNER START')
		return

	def onCompleteRunner(self):
		LOG_INFO('EVENT RUNNER COMPLETE')
		return

	def onStopRunner(self):
		LOG_INFO('EVENT RUNNER STOP')
		return

	def onErrorRunner(self, error=None):
		LOG_ERROR('EVENT RUNNER ERROR    : ')
		LOG_EXCEPTION(LOG_LEVEL_DEBUG, error)
		return

	def onEvent(self, event, headers=None, body=None):
		LOG_INFO('EVENT                 : {}, {}, {}'.format(
			event,
			headers,
			body,
		))
		return

	def onEventSuccess(self, event, headers=None, body=None, response=None):
		LOG_INFO('EVENT SUCCESS         : {}, {}, {}, {}'.format(
			event,
			headers,
			body,
			response
		))
		return

	def onEventError(self, event, headers=None, body=None, error=None):
		LOG_ERROR('EVENT ERROR           : {}, {}, {}'.format(
			event,
			headers,
			body,
		))
		if error:
			LOG_EXCEPTION(LOG_LEVEL_DEBUG, error)
		return
