# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from cgi import parse_header
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence, Mapping
from json import dumps
from typing import Optional, Any

__all__ = (
	'Stauts',
	'StatusHandler',
)

class Request:
	"""Request"""
	def __init__(self, method, uri, qs=None, body=None, format=None, charset=None, headers=None) -> None:
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
	def __init__(self, status, message=None, body=None, format=None, charset=None, headers=None) -> None:
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
	def do_GET(self):
		try:
			url = urlparse(self.path)
			uri = url.path
			qs = parse_qs(unquote(url.params)) if url.params else None
			body = None
			format = None
			charset = None
			if 'Content-Length' in self.headers.keys():
				body = self.rfile.read(int(self.headers('Content-Length')))
				if self.headers('Content-Type'):
					args, kwargs = parse_header(self.headers('Content-Type'))
					format = args[0] if args[0] else None
					charset = kwargs['charset'] if 'charset' in kwargs.keys() else None
			headers = {}
			for key, value in self.headers.items():
				headers[key] = parse_header(value)
			request = Request(
				method=self.command,
				uri=uri,
				qs=qs,
				body=body,
				format=format,
				charset=charset,
				headers=headers
			)
			status = self.server.handler.onStatus()
			if status:
				if isinstance(status, str):
					response = Response(
						200,
						body=status.encode('utf-8'),
						format='text/plain',
						charset='utf-8',
					)
				else:
					response = Response(
						200,
						body=dumps(status).encode('utf-8'),
						format='text/plain',
						charset='utf-8',
					)
			else:
				response = Response(200)
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
			for keyword, value in response.headers if response.headers else []:
				self.send_header(keyword, value)
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
		self.server.handler.onResponse(code, size)
		return


class StatusHandler(metaclass=ABCMeta):
	@abstractmethod
	def onStatus(self) -> Optional[Any]:
		pass

	@abstractmethod
	def onResponse(self, code, size=None):
		pass

class Status(object): 
	"""Status for Worker with HTTP Server"""
	def __init__(self, handler: StatusHandler, port : int = 9999, host : str = '127.0.0.1') -> None:
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
