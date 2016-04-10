import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource

from crashprotocol import ServerProtocol, VipProtocol

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    ''' Factory for normal clients '''
    factory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = ServerProtocol

    resource = WebSocketResource(factory)

    # we server static files under "/" ..
    root = File(".")

    # and our WebSocket server under "/ws"
    root.putChild(u"ws", resource)

    # both under one Twisted Web Site
    site = Site(root)
    reactor.listenTCP(8080, site)

    ''' Factory for VIP '''
    vipfactory = WebSocketServerFactory(u'ws://127.0.0.1:9000')
    vipfactory.protocol = VipProtocol
    reactor.listenTCP(9000, vipfactory)

    reactor.run()
