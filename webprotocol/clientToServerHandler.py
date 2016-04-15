import time

from twisted.internet import reactor, defer, threads

from DH_Key_Exchange import DH

class clientToServerHandler:
	@classmethod
	def waitForTurn(self):


class vipToServerHandler:
	connection = None

	@classmethod
	def subscribe(self, serverConnection):
		if self.connection is not None:
			return False
		self.connection = serverConnection
		return True

	@classmethod
	def unsubscribe(self, serverConnection):
		if self.connection is serverConnection:
			self.connection = None

	@classmethod
	def 