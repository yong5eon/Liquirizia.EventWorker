# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	EventWorkerContext,
	EventWorker,
	EventInvoker,
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
	EventRunnerPool,
	ThreadEventRunnerPool,
	ProcessEventRunnerPool,
)

from signal import signal, SIGINT
from time import sleep
from random import randint


class SampleEventRunnerComplete(EventRunnerComplete):
	def __call__(self, completion):
		print('Complete : {}'.format(completion))
		return
	
class SampleEventRunnerError(EventRunnerError):
	def __call__(self, error: BaseException):
		print('Error : {}'.format(str(error)))
	

class SampleEventRunner(EventRunner):
	def run(self, body):
		print('Run : {}'.format(body))
		if body % 2 == 0:
			raise ValueError('Even number')
		return body


class SampleEventInvoker(EventInvoker):
	def __init__(self, context: EventWorkerContext, pool: EventRunnerPool):
		self.context = context
		self.pool = pool
		return
	def run(self):
		while self.context:
			self.pool.add(SampleEventRunner, randint(0, 10), SampleEventRunnerComplete(), SampleEventRunnerError())
			sleep(1)
		return
	def stop(self):
		pass


if __name__ == '__main__':
	MAX = 2
	worker = EventWorker(ThreadEventRunnerPool(MAX), SampleEventInvoker)
	def stop(signal, frame):
		print('EventWorker stopping...')
		worker.stop()
		return
	signal(SIGINT, stop)
	print('EventWorker running until break with keyboard interrupt...')
	worker.run()
	print('EventWorker stopped...')
