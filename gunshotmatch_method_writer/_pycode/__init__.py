"""
Utilities parsing and analyzing Python code.
"""

# stdlib
from importlib import import_module
from typing import Any, Dict, List, Tuple

# this package
from .parser import Parser

__all__ = ("ModuleAnalyzer", )


class ModuleAnalyzer:  # noqa: D101
	attr_docs: Dict[Tuple[str, str], List[str]]

	# cache for analyzer objects -- caches both by module and file name
	cache: Dict[Tuple[str, str], Any] = {}

	@staticmethod
	def get_module_source(modname: str) -> Tuple[str, str]:
		"""Try to find the source code for a module.

		Returns ('filename', 'source'). One of it can be None if
		no filename or source found
		"""

		mod = import_module(modname)
		loader = getattr(mod, "__loader__", None)

		if loader and getattr(loader, "get_source", None):
			source = loader.get_source(modname)
			if source:
				return getattr(mod, "__file__", "<string>"), source

		raise ValueError("no source found for module %r" % modname)

	@classmethod
	def for_module(cls, modname: str) -> "ModuleAnalyzer":  # noqa: D102

		filename, source = cls.get_module_source(modname)
		return cls(source, modname, filename or "<string>")

	def __init__(self, source: str, modname: str, srcname: str) -> None:
		self.srcname = srcname  # name of the source file

		# cache the source code as well
		self.code = source

		self._analyzed = False

	def analyze(self) -> None:
		"""Analyze the source code."""
		if self._analyzed:
			return

		try:
			parser = Parser(self.code)
			parser.parse()

			self.attr_docs = {}
			for (scope, comment) in parser.comments.items():
				if comment:
					self.attr_docs[scope] = comment.splitlines() + ['']
				else:
					self.attr_docs[scope] = ['']

			self._analyzed = True
		except Exception as exc:
			raise ValueError(f'parsing {self.srcname!r} failed: {exc!r}') from exc
