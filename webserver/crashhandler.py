import time
from threading import Lock, Thread
from collections import deque
from twisted.internet import reactor, defer, threads

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
    @classmethod
    def sendNumbers(self):
        pass
