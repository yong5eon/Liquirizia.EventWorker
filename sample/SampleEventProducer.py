# -*- coding: utf-8 -*-

from Liquirizia.EventBroker import EventBrokerHelper
from Liquirizia.EventBroker.Errors import *
from Liquirizia.EventBroker.Implements.RabbitMQ import (
	Configuration,
	Connection,
)
import Liquirizia.Serializer.Implements.Text
import Liquirizia.Serializer.Implements.JavaScriptObjectNotation

from random import randint
from uuid import uuid4

if __name__ == '__main__':

	# LOG_INITIALIZE(LOG_LEVEL_DEBUG)

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

	for i in range(0, 10):
		val = randint(0, 1000)
		EventBrokerHelper.Publish('Sample', 'topic.sample', event='event.sample', body=str(val), format='text/plain', charset='utf-8')
		print('PUBS : {}'.format(val))

	for i in range(0, 10):
		try:
			val = randint(0, 1000)
			rep = 'queue.sample.{}'.format(uuid4())
			EventBrokerHelper.CreateQueue('Sample', rep, persistent=False)
			id = EventBrokerHelper.Publish('Sample', topic='topic.sample', event='event.sample', body=str(val), format='text/plain', charset='utf-8', headers={
				'X-Reply-Broker': 'Sample',
				'X-Reply-Broker-Queue': rep
			})
			res = EventBrokerHelper.Receive('Sample', rep, timeout=1000)
			print('CALL : {}, {}'.format(val, res))
		except TimeoutError:
			pass

	for i in range(0, 10):
		val = {
			'a': randint(0, 1000),
			'b': randint(0, 1000),
		}
		EventBrokerHelper.Publish('Sample', 'topic.sample', event='event.sample.compute.add', body=val, format='application/json', charset='utf-8')
		print('PUBS : {}'.format(val))

	for i in range(0, 10):
		try:
			val = {
				'a': randint(0, 1000),
				'b': randint(0, 1000),
			}
			rep = 'queue.sample.compute.add.{}'.format(uuid4())
			EventBrokerHelper.CreateQueue('Sample', rep, persistent=False)
			id = EventBrokerHelper.Publish('Sample', topic='topic.sample', event='event.sample.compute.add', body=val, format='application/json', charset='utf-8', headers={
				'X-Reply-Broker': 'Sample',
				'X-Reply-Broker-Queue': rep
			})
			res = EventBrokerHelper.Receive('Sample', rep, timeout=1000)
			print('CALL : {} + {} = {}'.format(val['a'], val['b'], res))
		except TimeoutError as e:
			pass

	for i in range(0, 10):
		val = {
			'a': randint(0, 1000),
			'b': randint(0, 1000),
		}
		EventBrokerHelper.Publish('Sample', 'topic.sample', event='event.sample.compute.sub', body=val, format='application/json', charset='utf-8')
		print('PUBS : {}'.format(val))

	EventBrokerHelper.CreateQueue('Sample', 'queue.sample.compute.sub.reply', persistent=False)
	for i in range(0, 10):
		try:
			val = {
				'a': randint(0, 1000),
				'b': randint(0, 1000),
			}
			rep = 'queue.sample.compute.sub.{}'.format(uuid4())
			EventBrokerHelper.CreateQueue('Sample', rep, persistent=False)
			id = EventBrokerHelper.Publish('Sample', topic='topic.sample', event='event.sample.compute.sub', body=val, format='application/json', charset='utf-8', headers={
				'X-Reply-Broker': 'Sample',
				'X-Reply-Broker-Queue': rep
			})
			res = EventBrokerHelper.Receive('Sample', rep, timeout=1000)
			print('CALL : {} - {} = {}'.format(val['a'], val['b'], res))
		except TimeoutError as e:
			pass
