from autobahn.twisted.websocket import WebSocketClientProtocol
from twisted.internet import reactor

from handlers import VipHandler, ClientHandler

class VipClientProtocol(WebSocketClientProtocol):
    """Protocol for VIP client"""
    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {0}".format(payload.decode('utf8')))
            key, value = str(payload).split('=')
            if key == 'key':
                VipHandler.us_auth(self, value)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class ClientProtocol(WebSocketClientProtocol):
    """Protocol for normal clients"""
    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = str(payload)
            print("Text message received: {0}".format(payload.decode('utf8')))
            key, value = str(payload).split('=')
            if key == 'g':
                ClientHandler.setG(value)
            elif key == 'p':
                ClientHandler.setP(value)
            if ClientHandler.gotBothPrimes():
                print('Send turn_ready to server')
                # it appears to send only when the method returns.
                # Hack by using reactor.callLater
                self.sendMessage('turn_ready', False)
                reactor.callLater(1, ClientHandler.us_auth, self)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
