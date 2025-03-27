# -*- coding: utf-8 -*-

from .Server import (
	Server,
	Request,
	Response,
	Handler,
)
from ...Context import Context

from threading import Thread
from abc import ABCMeta, abstractmethod
from json import dumps

__all__ = (
)


class JavaScriptObjectNotationStatusHandler(Handler):
	def __call__(self, request: Request) -> Response:
		ctx = Context()
		buffer = dumps(ctx.status(), ensure_ascii=False).encode('utf-8')
		return Response(
			status=200,
			body=buffer,
			format='application/json',
			charset='utf-8',
			headers={
				'Content-Type': 'application/json; charset=utf-8',
				'Content-Length': str(len(buffer)),
			},
		)


class StatusChecker(object):
	def __init__(self, handler: Handler = JavaScriptObjectNotationStatusHandler(), port: int = 9999, host: str = '127.0.0.1'):
		self.server = Server(
			handler=handler,
			port=port,
			host=host,
		)
		return

	def __run__(self):
		self.server.run()
		return

	def start(self):
		self.checker = Thread(target=self.__run__)
		self.checker.start()
		return

	def run(self):
		self.checker = Thread(target=self.__run__)
		self.checker.start()
		self.checker.join()
		return

	def stop(self):
		self.server.stop()
		self.checker.join()
		return