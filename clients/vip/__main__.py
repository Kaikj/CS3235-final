import sys

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory

from clients.protocols import VipClientProtocol

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    coordinator = '127.0.0.1'
    if len(sys.argv) > 1:
        coordinator = sys.argv[1]

    factory = WebSocketClientFactory(u"ws://{}:9000".format(coordinator), debug=False)
    factory.protocol = VipClientProtocol

    reactor.connectTCP(coordinator, 9000, factory)
    reactor.run()
