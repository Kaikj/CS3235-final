import sys

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory

from clients.protocols import ClientProtocol

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    coordinator = '127.0.0.1'
    if len(sys.argv) > 1:
        coordinator = sys.argv[1]
    
    factory = WebSocketClientFactory(u"ws://{}:8080/ws".format(coordinator), debug=False)
    factory.protocol = ClientProtocol

    reactor.connectTCP(coordinator, 8080, factory)
    reactor.run()
