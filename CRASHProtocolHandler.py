import time
from threading import Lock, Thread
from collections import deque
from twisted.internet import reactor, defer, threads

class CrashProtocolHandler:
    promiseQueue = deque([])
    CRASHLock = Lock()

    @classmethod
    def initAuth(self):
        turnPromise = defer.Deferred()
        self.promiseQueue.append(turnPromise)
        Thread(target=self.waitForTurn).start()
        return turnPromise

    @classmethod
    def waitForTurn(self):
        # block other clients who try to authenticate
        self.CRASHLock.acquire()
        # tell client its his/her turn
        self.promiseQueue.popleft().callback(None)

    @classmethod
    def startAuth(self):
        authPromise = defer.Deferred()
        Thread(target=self.CRASHAuth, kwargs={ 'promise': authPromise }).start()
        return authPromise

    @classmethod
    def CRASHAuth(self, promise):
        # Invoke CRASH protocol here
        time.sleep(2)
        # release lock to allow other client to authenticate
        self.CRASHLock.release()
        promise.callback(True)
