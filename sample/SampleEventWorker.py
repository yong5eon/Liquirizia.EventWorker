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
		if 'X-Reply-Broker' in self.headers.keys() and 'X-Reply-Broker-Queue' in self.headers.keys():
			EventBrokerHelper.Send(
				self.headers['X-Reply-Broker'], 
				queue=self.headers['X-Reply-Broker-Queue'], 
				event=self.type, 
				body=body, 
				format='text/plain', 
				charset='utf-8'
			)
		return


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

	worker = EventWorker(SampleEventWorkerHandler())
	worker.add(EventRunnerProperties(
		SampleRunner,
		type=TypeWorker('event.sample', 'Sample', 'queue.sample'),
	))
	worker.load('Liquirizia.EventWorker/sample/*.conf')
	# worker.load('.', pattern='*.conf')

	worker.run()
