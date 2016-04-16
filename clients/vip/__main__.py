import sys

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory

from clients.protocols import VipClientProtocol

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = VipClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
