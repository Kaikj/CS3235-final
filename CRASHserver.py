import sys
import threading

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource

from CRASHProtocolHandler import CrashProtocolHandler

class CRASHServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print(self.peer)
        # protocol, ip, port = self.peer.split(':')
        self.initAuthenticate()

    def initAuthenticate(self):
        turn_promise = CrashProtocolHandler.initAuth()
        turn_promise.addCallback(self.startAuthenticate)

    def startAuthenticate(self, result):
        self.sendMessage('yourTurn', False)
        print('Authenticating...')
        # wait to receive back from client
        auth_promise = CrashProtocolHandler.startAuth()
        auth_promise.addCallback(self.onAuthSuccess)

    def onAuthSuccess(self, success):
        print('Authentication successful')
        if success:
            self.sendMessage('url:http://www.google.com', False)

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)
        if str(payload) == 'authSuccess':
            self.onAuthSuccess(self)

    def onClose(self, wasClean, code, reason):
        print(reason)


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = CRASHServerProtocol

    resource = WebSocketResource(factory)

    # we server static files under "/" ..
    root = File(".")

    # and our WebSocket server under "/ws"
    root.putChild(u"ws", resource)

    # both under one Twisted Web Site
    site = Site(root)
    reactor.listenTCP(8080, site)

    reactor.run()
