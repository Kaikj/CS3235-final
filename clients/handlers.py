import abc
import us_receiver
import us_sender
from DH_Key_Exchange import DH
from twisted.internet import reactor, defer, threads

class VipHandler:
    """
    Module that acts as a layer between UltraSound module and the websocket module
    on the VIP side

    """

    @classmethod
    def us_auth(self, server_connection, key):
        #initialise and run sender
        sender = us_sender.UsSender()
        sender.run(str(key))
        #initialise and run receiver after sending
        receiver = us_receiver.UsReceiver()
        clientPubKey = receiver.run()
        server_connection.sendMessage(str(clientPubKey), False)


class ClientHandler:
    """Module that acts as a layer between UltraSound module and the websocket module"""
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
    def us_auth(self, server_connection):
        # ultrasound auth here
        #initialise and run receiver
        receiver = us_receiver.UsReceiver()
        vipPubKey = receiver.run()
        print('g^a mod p received: {}'.format(vipPubKey))
        # based on DH_Key_Exchange.py examples
        clientDH = DH()
        clientPrivKey = clientDH.computePrivateKey(clientDH.keylength)
        clientPubKey = clientDH.computePublicKey(self.g, clientPrivKey, self.p)
        print('g^b mod p generated: {}'.format(clientPubKey))
        #initialise and run sender
        sender = us_sender.UsSender()
        sender.run(str(clientPubKey))
        print('g^ab mod p: {}'.format(pow(vipPubKey, clientPrivKey, self.p)))
        clientSymKey = clientDH.computeSymmetricKey(vipPubKey, clientPrivKey, self.p)
        self.p = None
        self.g = None
        # haven't decided what to do after the key exchange
        print (clientSymKey)
