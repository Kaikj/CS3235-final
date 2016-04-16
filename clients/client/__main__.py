import sys

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory

from clients.protocols import ClientProtocol

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:8080/ws", debug=False)
    factory.protocol = ClientProtocol

    reactor.connectTCP("127.0.0.1", 8080, factory)
    reactor.run()
