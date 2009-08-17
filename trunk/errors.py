"""errors.py
Exceptions"""
__all__ = ["PlatformException", "CouldNotSendRequest", "InvalidSPARQLSelectResultSyntax", "InvalidCommandParameters", "AbstractClassError"]
class PlatformException(Exception): pass
class CouldNotSendRequest(PlatformException): pass
class InvalidSPARQLSelectResultSyntax(PlatformException): pass
class InvalidCommandParameters(PlatformException): pass
class AbstractClassError(PlatformException):
	def __init__(self, cls, *others):
		self.cls = cls
		self.others = others
	def __str__(self):
		return "%s is an abstract class and cannot be instantaniated (did you mean: %s)" % (self.cls, ", ".join(self.others))
