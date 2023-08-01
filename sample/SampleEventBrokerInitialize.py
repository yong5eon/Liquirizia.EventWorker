# -*- coding: utf-8 -*-

from impm import ImportModule

ImportModule('Liquirizia', 'Liquirizia/src')
ImportModule('Liquirizia.EventBroker', 'Liquirizia.EventBroker/src')
ImportModule('Liquirizia.EventBroker.Implements.RabbitMQ', 'Liquirizia.EventBroker.Implements.RabbitMQ/src')
ImportModule('Liquirizia.EventRunner', 'Liquirizia.EventRunner/src')
ImportModule('Liquirizia.EventWorker', 'Liquirizia.EventWorker/src')

from Liquirizia.EventBroker import EventBrokerHelper
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
)


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
	queue.declare('queue.complete')
	queue.declare('queue.error')
	queue.bind('topic.error.route', '*')
	queue.declare('queue.sample')
	queue.bind('topic.sample', 'event.sample')
	queue.declare('queue.sample.compute.add')
	queue.bind('topic.sample', 'event.sample.compute.add')
	queue.declare('queue.sample.compute.sub')
	queue.bind('topic.sample', 'event.sample.compute.sub')
