from autobahn.twisted.websocket import WebSocketServerProtocol
from crashhandler import ClientHandler, VipHandler

class ServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print(self.peer)
        # protocol, ip, port = self.peer.split(':')
        # self.sendMessage('Please wait for your turn', False)
        ClientHandler.initAuth(self)

    def onMessage(self, payload, isBinary):
        # self.sendMessage(payload, isBinary)
        print("Text message received: {}".format(payload.decode('utf8')))
        if str(payload) == 'turn_ready':
            print("Client ready. Start authenticating.")
            ClientHandler.startAuth(self)

    def onClose(self, wasClean, code, reason):
        print(reason)


class VipProtocol(WebSocketServerProtocol):
    def onOpen(self):
        print('VIP connects.')
        print(self.peer)
        success = VipHandler.subscribe(self)
        if not success:
            print("no success???")
            self.dropConnection()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
            str_payload = str(payload)
            try:
                key = int(str_payload)
                VipHandler.onAuthSuccess(key)
            except ValueError, e:
                # raise e
                pass

    def onClose(self, wasClean, code, reason):
        VipHandler.unsubscribe(self)
        print(reason)
