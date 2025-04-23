# -*- coding: utf-8 -*-

from os.path import splitext, split
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib import import_module
from pkgutil import walk_packages

__all__ = (
	'Loader',
)

class Loader(object):
	def __call__(self, mod: str = None, path: str = None, ext: str = 'py'):
		if mod:
			self.mod(mod)
		if path:
			ps = Path(path).rglob('*.{}'.format(ext))
			for p in ps if ps else []:
				p = self.path(str(p))
		return
	
	def path(self, path):
		head, tail = split(path)
		file, ext = splitext(tail)
		head = head.replace('\\', '.').replace('/', '.')
		mod = '{}.{}'.format(head, file)
		loader = SourceFileLoader(mod, path)
		mo = loader.load_module()
		if not mo:
			return None
		return mo
	
	def mod(self, mod):
		pkg = import_module(mod)
		for _, name, isPackage in walk_packages(pkg.__path__):
			fullname = pkg.__name__ + '.' + name
			if isPackage:
				self.mod(fullname)
				continue
			import_module(fullname)
		return
