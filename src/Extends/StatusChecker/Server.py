# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from cgi import parse_header
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence, Mapping
from json import dumps
from typing import Optional, Any, Dict, Tuple

__all__ = (
	'Request',
	'Response',
	'Handler',
	'Server',
)

class Request:
	"""Request"""
	def __init__(
		self,
		method: str, 
		uri: str, 
		qs: Dict[str, str] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		headers: Dict[str, str]= None
	):
		self.method = method
		self.uri = uri
		self.qs = qs
		self.body = body
		self.format = format
		self.charset = charset
		self.size = len(body) if body else 0
		self.headers = headers
		return

class Response:
	"""Response"""
	def __init__(
		self,
		status: int,
		message: str = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		headers: Dict[str, str] = None):
		self.status = status
		self.message = message
		self.body = body
		self.format = format
		self.charset = charset
		self.size = len(body) if body else 0
		self.headers = headers
		return

	
class RequestHandler(BaseHTTPRequestHandler):
	"""Request Handler"""

	def strip(self, value: str, prefix: str = '"', postfix: str = '"'):
		value = value.strip()
		if len(value) and prefix:
			if value[0] == prefix: value = value[1:]
		if len(value) and postfix:
			if value[-1:] == postfix: value = value[:-1]
		return value

	def parse(self, value: str, sep: str = ';', paramsep: str = ',') -> Tuple[str, Dict[str, str]]:
		ts = value.strip().split(sep, maxsplit=1)
		val = self.strip(ts[0])
		params = {}
		if len(ts) > 1:
			for p in ts[1].strip().split(paramsep):
				ps = p.strip().split('=')
				params[self.strip(ps[0])] = self.strip(ps[1]) if len(ps) > 1 else None
		return val, params

	def do_GET(self):
		try:
			url = urlparse(self.path)
			uri = url.path
			qs = parse_qs(unquote(url.params)) if url.params else None
			body = None
			format = None
			charset = None
			headers = {}
			for k, v in self.headers.items() if self.headers else []:
				if k == 'Content-Length':
					body = self.rfile.read(int(self.headers('Content-Length')))
					continue
				if k == 'Content-Type':
					args, kwargs = self.parse(self.headers('Content-Type'))
					format = args[0] if args[0] else None
					charset = kwargs['charset'] if 'charset' in kwargs.keys() else None
					continue
				headers[k] = v
			request = Request(
				method=self.command,
				uri=uri,
				qs=qs,
				body=body,
				format=format,
				charset=charset,
				headers=headers
			)
			response = self.server.handler(request)
		except Exception as e:
			body = str(e).encode('utf-8')
			response = Response(
				503,
				'Service Unavailable',
				body=body,
				format='text/plain',
				charset='utf-8',
			)
		finally:
			self.send_response(response.status, response.message)
			for k, v in response.headers.items() if response.headers else []:
				self.send_header(k, v)
			if response.body:
				self.send_header('Content-Length', response.size)
				if response.format:
					self.send_header('Content-Type', '{}{}'.format(
						response.format,
						'; charset={}'.format(response.charset) if response.charset else ''
					))
			self.end_headers()
			self.flush_headers()
			if response.body:
				self.wfile.write(response.body)
		return

	def log_request(self, code, size=None):
		pass


class Handler(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, request: Request) -> Response:
		raise NotImplementedError('{} must be implemented __call__ method'.format(self.__class__.__name__))


class Server(object): 
	"""Status for Worker with HTTP Server"""
	def __init__(self, handler: Handler, port : int = 9999, host : str = '127.0.0.1') -> None:
		self.httpd = HTTPServer((host, port), RequestHandler)
		self.httpd.handler = handler
		return
	
	def run(self):
		self.httpd.serve_forever()
		return
	
	def stop(self):
		self.httpd.server_close()
		self.httpd.shutdown()
		return
	
	def shutdown(self):
		self.httpd.server_close()
		self.httpd.shutdown()
		return
