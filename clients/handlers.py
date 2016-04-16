import abc
import us_receiver
import us_sender
from DH_Key_Exchange import DH
from twisted.internet import reactor, defer, threads

class _Handler:
    g = None
    p = None
    privateKey = None

    @classmethod
    def setG(self, g):
        self.g = long(g)

    @classmethod
    def setP(self, p):
        self.p = long(p)

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
        sender = us_sender.UsSender()
        sender.run(str(vipPubKey))
        #initialise and run receiver after sending
        receiver = us_receiver.UsReceiver()
        clientPubKey = receiver.run()
        vipSymKey = vipDH.computeSymmetricKey(vipPrivKey, vipPubKey, self.p)
        self.p = None
        self.g = None
        server_connection.sendMessage(str(vipSymKey), False)


class ClientHandler(_Handler):
    """Module that acts as a layer between UltraSound module and the websocket module"""

    @classmethod
    def us_auth(self, server_connection):
        # ultrasound auth here
        #initialise and run receiver
        receiver = us_receiver.UsReceiver()
        vipPubKey = receiver.run()
        # based on DH_Key_Exchange.py examples
        clientDH = DH()
        clientPrivKey = clientDH.computePrivateKey(clientDH.keylength)
        clientPubKey = clientDH.computePublicKey(self.g, clientPrivKey, self.p)
        #initialise and run sender
        sender = us_sender.UsSender()
        sender.run(str(clientPubKey))
        clientSymKey = clientDH.computeSymmetricKey(clientPrivKey, clientPubKey, self.p)
        self.p = None
        self.g = None
        # haven't decided what to do after the key exchange
        print (clientSymKey)
