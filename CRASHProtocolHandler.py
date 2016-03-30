import time
from threading import Lock, Thread
from collections import deque
from twisted.internet import reactor, defer, threads

class CrashProtocolHandler:
    promiseQueue = deque([])
    CRASHLock = Lock()
    running = False

    @classmethod
    def initAuth(self):
        turnPromise = defer.Deferred()
        self.promiseQueue.append(turnPromise)
        if not self.running:
            Thread(target=self.run).start()
        return turnPromise

    @classmethod
    def run(self):
        self.running = True
        while len(self.promiseQueue) > 0:
            with self.CRASHLock:
                self.promiseQueue.popleft().callback(None) # tell client its his/her turn
        self.running = False

    @classmethod
    def startAuth(self):
        authPromise = defer.Deferred()
        Thread(target=self.CRASHAuth, kwargs={ 'promise': authPromise }).start()
        return authPromise

    @classmethod
    def CRASHAuth(self, promise):
        # Invoke CRASH protocol here
        time.sleep(2)
        promise.callback(True)
