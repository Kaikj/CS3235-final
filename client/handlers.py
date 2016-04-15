import abc
from twisted.internet import reactor, defer, threads

class _Handler:
    g = None
    p = None

    @classmethod
    def setG(self, g):
        self.g = g

    @classmethod
    def setP(self, p):
        self.p = p

    @classmethod
    def gotBothPrimes(self):
        return self.p != None and self.g != None

    @classmethod
    @abc.abstractmethod
    def us_auth(self, server_connection):
        return

class VipHandler(_Handler):
    """Module that acts as a layer between UltraSound module and the websocket module"""

    @classmethod
    def us_auth(self, server_connection):
        # ultrasound auth here
        self.p = None
        self.g = None
        server_connection.sendMessage('5000', False) # replace '5000' with the shared key

class ClientHandler(_Handler):
    """Module that acts as a layer between UltraSound module and the websocket module"""

    @classmethod
    def us_auth(self, server_connection):
        # ultrasound auth here
        self.p = None
        self.g = None
        # haven't decided what to do after the key exchange
        print ('the key?')
