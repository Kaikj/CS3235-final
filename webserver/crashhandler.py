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
        self.clientQueue.append(client)
        Thread(target=self.waitForTurn).start()

    @classmethod
    def waitForTurn(self):
        # block other clients who try to authenticate
        self.CRASHLock.acquire()
        # tell client its his/her turn
        self.clientQueue.popleft().sendMessage('yourTurn', False)
        # wait to receive back from client

    @classmethod
    def startAuth(self, client):
        print('Authenticating...')
        keyPromise = VipHandler.CRASHAuth()
        keyPromise.addCallback(self.gotKey, client=client)

    @classmethod
    def gotKey(self, result, client):
        '''
        result is the key
        '''
        # release lock to allow other client to authenticate
        self.CRASHLock.release()
        # TODO: handle exceptional case
        print('Authentication successful')
        client.sendMessage('url:http://www.google.com', False)

class VipHandler:
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
        if self.connection is not vip_connection:
            pass
        self.connection = None

    @classmethod
    def CRASHAuth(self):
        # ensure we only authenticate one at a time
        self.CRASHLock.acquire()

        self.keyPromise = defer.Deferred()
        '''
        # generate DHKE
        # keygen = DH()

        # send to VIP
        self.connection.sendMessage('g=' + keygen.generator, False)
        self.connection.sendMessage('p=' + keygen.prime, False)
        self.connection.sendMessage('public=' + keygen.publicKey, False)
        # wait for g^b mod p
        '''
        # Dummy wait, to be replaced with the actual protocol above
        reactor.callLater(2, self.onAuthSuccess, 0)
        return self.keyPromise

    @classmethod
    def onAuthSuccess(self, key):
        self.keyPromise.callback(key)
        self.CRASHLock.release()
