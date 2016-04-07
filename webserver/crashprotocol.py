import threading

from autobahn.twisted.websocket import WebSocketServerProtocol
from crashhandler import ClientHandler, VipHandler

class ServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print(self.peer)
        # protocol, ip, port = self.peer.split(':')
        self.initAuthenticate()

    def initAuthenticate(self):
        turn_promise = ClientHandler.initAuth()
        turn_promise.addCallback(self.startAuthenticate)

    def startAuthenticate(self, result):
        self.sendMessage('yourTurn', False)
        print('Authenticating...')
        # wait to receive back from client
        auth_promise = ClientHandler.startAuth()
        auth_promise.addCallback(self.onAuthSuccess)

    def onAuthSuccess(self, success):
        print('Authentication successful')
        if success:
            self.sendMessage('url:http://www.google.com', False)

    def onMessage(self, payload, isBinary):
        self.sendMessage(payload, isBinary)
        if str(payload) == 'authSuccess':
            self.onAuthSuccess(self)

    def onClose(self, wasClean, code, reason):
        print(reason)


class VipProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('VIP connects.')
        print(self.peer)
        VipHandler.sendNumbers()
