# -*- coding: utf-8 -*-

from Liquirizia.EventWorker import (
	EventRunner,
	EventRunnerComplete,
	EventRunnerError,
	EventProperties,
)

from Liquirizia.Logger import (
	LOG_DEBUG,
	LOG_ERROR,
	LOG_INFO,
)

__all__ = (
	'Add',
	'Sub',
	'Mul',
	'Div',
	'Mod',
	'Complete',
	'Error',
)


class Complete(EventRunnerComplete):
	def __call__(self, completion):
		LOG_INFO('Complete : {}'.format(completion))
		return
	
class Error(EventRunnerError):
	def __call__(self, error: BaseException):
		LOG_ERROR('Error : {}'.format(str(error)), e=error)
		return


@EventProperties(
	event='+',
	completes=Complete(),
	errors=Error(),
)
class Add(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} + {}'.format(a, b))
		return a + b

@EventProperties(
	event='-',
	completes=Complete(),
	errors=Error(),
)
class Sub(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} - {}'.format(a, b))
		return a - b

@EventProperties(
	event='*',
	completes=Complete(),
	errors=Error(),
)
class Mul(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} * {}'.format(a, b))
		return a * b

@EventProperties(
	event='/',
	completes=Complete(),
	errors=Error(),
)
class Div(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} / {}'.format(a, b))
		return a / b


@EventProperties(
	event='%',
	completes=Complete(),
	errors=Error(),
)
class Mod(EventRunner):
	def run(self, a: int , b: int):
		LOG_DEBUG('Run : {} % {}'.format(a, b))
		return a % b
