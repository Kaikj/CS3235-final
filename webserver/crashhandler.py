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
        keyPromise = VipHandler.CRASHAuth(client.keygen.generator, client.keygen.prime)
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
    def CRASHAuth(self, g, p):
        # ensure we only authenticate one at a time
        self.CRASHLock.acquire()

        self.keyPromise = defer.Deferred()
        if self.connection:
            # send to VIP
            self.connection.sendMessage('g=' + str(g), False)
            self.connection.sendMessage('p=' + str(p), False)
            # self.connection.sendMessage('public=' + keygen.publicKey, False)
            # wait for g^b mod p
        else:
            # Dummy wait, to be replaced with the actual protocol above
            reactor.callLater(2, self.onAuthSuccess, 0)

        return self.keyPromise

    @classmethod
    def onAuthSuccess(self, key):
        self.keyPromise.callback(key)
        self.CRASHLock.release()
