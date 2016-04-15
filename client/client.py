from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from handler import Handler

class VipClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            key, value = str(payload).split('=')
            if key == 'g':
                Handler.setG(value)
            elif key == 'p':
                Handler.setP(value)
            if Handler.gotBothPrimes():
                Handler.us_auth(self)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = VipClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()
