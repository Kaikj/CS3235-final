import time
from threading import Lock, Thread
from collections import deque

from twisted.internet import reactor, defer, threads

from DH_Key_Exchange import DH

class ClientHandler:
    clientQueue = deque([])
    CRASHLock = Lock()

    @classmethod
    def initAuth(self, client):
        client.keygen = DH()
        self.clientQueue.append(client)
        Thread(target=self.waitForTurn).start()

    @classmethod
    def waitForTurn(self):
        # block other clients who try to authenticate
        self.CRASHLock.acquire()
        # send the g and p to client
        client = self.clientQueue.popleft()
        client.sendMessage('g=' + str(client.keygen.generator))
        client.sendMessage('p=' + str(client.keygen.prime))
        # wait to receive back from client

    @classmethod
    def startAuth(self, client):
        print('Authenticating...')
        a = client.keygen.computePrivateKey(client.keygen.keylength)
        publicKey = client.keygen.computePublicKey(client.keygen.generator, a, client.keygen.prime)
        print('g^a mod p: {}'.format(publicKey))
        keyPromise = VipHandler.CRASHAuth(publicKey)
        keyPromise.addCallback(self.gotKey, client=client, privateKey = a)

    @classmethod
    def gotKey(self, result, client, privateKey):
        '''
        result is the other public key
        '''
        # release lock to allow other client to authenticate
        self.CRASHLock.release()
        # TODO: handle exceptional case
        print('g^b mod p received from VIP: %s'.format(result))
        print('g^ab mod p: %s'.format(str(pow(result, privateKey, keygen.prime))))
        symKey = client.keygen.computeSymmetricKey(result, privateKey, client.keygen.prime)
        print(symKey)
        print('Authentication successful')
        # client.sendMessage('url:http://www.google.com', False)

class VipHandler:
    connection = None
    CRASHLock = Lock()

    @classmethod
    def subscribe(self, vip_connection):
        '''
        Subscribes a connection (an instance of WebSocketServerProtocol) to
        authentication event.
        Return False if there is already another connection subscribed.
        '''
        if self.connection is not None:
            return False
        self.connection = vip_connection
        return True

    @classmethod
    def unsubscribe(self, vip_connection):
        if self.connection is vip_connection:
            self.connection = None

    @classmethod
    def CRASHAuth(self, publicKey):
        # ensure we only authenticate one at a time
        self.CRASHLock.acquire()

        self.keyPromise = defer.Deferred()
        if self.connection is not None:
            # send to VIP
            self.connection.sendMessage('key=' + str(publicKey), False)
            # wait for g^b mod p
        else:
            # Dummy wait, to be replaced with the actual protocol above
            reactor.callLater(2, self.onAuthSuccess, 0)

        return self.keyPromise

    @classmethod
    def onAuthSuccess(self, key):
        self.keyPromise.callback(key)
        self.CRASHLock.release()
