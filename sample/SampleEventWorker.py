# -*- coding: utf-8 -*-

from Liquirizia.EventBroker import EventBrokerHelper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
)

from Liquirizia.EventRunner import EventRunner, EventRunnerProperties
from Liquirizia.EventRunner.Types import EventWorker as TypeWorker

from Liquirizia.EventWorker import EventWorker

from SampleEventWorkerHandler import SampleEventWorkerHandler


class SampleRunner(EventRunner):
	def __init__(self, type: str, headers: dict = None):
		self.type = type
		self.headers = headers
		return

	def run(self, body=None):
		print('EVENT : {} - {} - {}'.format(self.type, self.headers, body))
		return body


if __name__ == '__main__':

	# 이벤트 브로커 설정
	EventBrokerHelper.Set(
		'Sample',
		Connection,
		Configuration(
			host='127.0.0.1',
			port=5672,
			username='guest',
			password='guest',
		)
	)

	broker = EventBrokerHelper.Get('Sample')

	topic = broker.topic()
	topic.declare('topic.sample', alter='topic.error.route', persistent=False)

	queue = broker.queue()
	queue.declare('queue.complete', persistent=False)
	queue.declare('queue.error', persistent=False)
	queue.bind('topic.error.route', '*')
	queue.declare('queue.sample', persistent=False)
	queue.bind('topic.sample', 'event.sample')
	queue.declare('queue.sample.compute.add', persistent=False)
	queue.bind('topic.sample', 'event.sample.compute.add')
	queue.declare('queue.sample.compute.sub', persistent=False)
	queue.bind('topic.sample', 'event.sample.compute.sub')

	worker = EventWorker(SampleEventWorkerHandler())
	worker.add(EventRunnerProperties(
		SampleRunner,
		type=TypeWorker('event.sample', 'Sample', 'queue.sample'),
	))
	worker.load('*.conf')
	# worker.load('.', pattern='*.conf')

	worker.run()
