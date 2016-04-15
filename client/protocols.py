from autobahn.twisted.websocket import WebSocketClientProtocol

from handlers import VipHandler

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
                VipHandler.setG(value)
            elif key == 'p':
                VipHandler.setP(value)
            if VipHandler.gotBothPrimes():
                VipHandler.us_auth(self)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


