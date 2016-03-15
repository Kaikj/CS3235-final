import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class CRASHServerProtocol(WebSocketServerProtocol):
    listOfInstances = []

    def onConnect(self, request):
        self.listOfInstances.append(self)

    def onOpen(self):
        print(self.peer)
        protocol, ip, port = self.peer.split(':')
        if ip == '127.0.0.1':
            print('Authenticating...')
            self.startAuthenticate()

    def startAuthenticate(self):
        for instance in self.listOfInstances:
            instance.sendMessage('yourTurn', False)
            # Invoke the ultrasound authentication here

    def onAuthSuccess(self, peer):
        for instance in self.listOfInstances:
            if instance is peer:
                instance.sendMessage('url:http://www.google.com', False)

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)
        if str(payload) == 'authSuccess':
            self.onAuthSuccess(self)

    def onClose(self, wasClean, code, reason):
        self.listOfInstances.remove(self)


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
