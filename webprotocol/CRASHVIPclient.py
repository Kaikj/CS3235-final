import sys
from optparse import OptionParser

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketClientFactory

from crashClientProtocol import vipToServerProtocol

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="The WebSocket URL", default="wss://127.0.0.1:9000")
    (options, args) = parser.parse_args()

    # create a WS server factory with our protocol
    ##
    factory = WebSocketClientFactory(options.url)
    factory.protocol = vipToServerProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()