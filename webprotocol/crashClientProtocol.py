from autobahn.twisted.websocket import WebSocketClientProtocol

class clientToServerProtocol(WebSocketClientProtocol):
	def dataReceived(self, )

class vipToServerProtocol(WebSocketClientProtocol):
	def onOpen(self):
		print(self.peer)
		success = vipToServerHandler.subscribe(self)
		if not success:
			self.dropConnection()

    def sendHello(self):
        self.sendMessage("Hello, world!".encode('utf8'))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
        reactor.callLater(1, self.sendHello)

    def onClose(self):
    	vipToServerHandler.unsubscribe(self)

