import abc
from ... import us_receiver
from ... import us_sender
from ... import DH_Key_Exchange
from twisted.internet import reactor, defer, threads

class _Handler:
    g = None
    p = None
    privateKey = None

    @classmethod
    def setG(self, g):
        self.g = g

    @classmethod
    def setP(self, p):
        self.p = p

    @classmethod
    def gotBothPrimes(self):
        return self.p != None and self.g != None

    @classmethod
    @abc.abstractmethod
    def us_auth(self, server_connection):
        return

class VipHandler(_Handler):
    """Module that acts as a layer between UltraSound module and the websocket module"""

    @classmethod
    def us_auth(self, server_connection):
        # ultrasound auth here
        # based on DH_Key_Exchange.py examples
        vipDH = DH()
        vipPrivKey = vipDH.computePrivateKey(vipDH.keylength)
        vipPubKey = vipDH.computePublicKey(self.g, vipPrivKey, self.p)
        #initialise and run sender
        sender = UsSender()
        sender.run(vipPubKey)
        #initialise and run receiver after sending
        receiver = UsReceiver()
        clientPubKey = receiver.run()
        vipSymKey = vipDH.computeSymmetricKey(vipPrivKey, vipPubKey, p)
        self.p = None
        self.g = None
        server_connection.sendMessage(vipSymKey, False) # replace '5000' with the shared key

class ClientHandler(_Handler):
    """Module that acts as a layer between UltraSound module and the websocket module"""

    @classmethod
    def us_auth(self, server_connection):
        # ultrasound auth here
        #initialise and run receiver
        receiver = UsReceiver()
        vipPubKey = receiver.run()
        # based on DH_Key_Exchange.py examples
        clientDH = DH()
        clientPrivKey = clientDH.computePrivateKey(clientDH.keylength)
        clientPubKey = clientDH.computePublicKey(self.g, clientPrivKey, self.p)
        #initialise and run sender
        sender = UsSender()
        sender.run(clientPubKey)
        clientSymKey = clientDH.computeSymmetricKey(clientPrivKey, clientPubKey, p)
        self.p = None
        self.g = None
        # haven't decided what to do after the key exchange
        print (clientSymKey)
