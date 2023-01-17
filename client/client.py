from xmlrpc.client import ServerProxy
from threading import Thread
from random import randint

def testing():
    proxy = ServerProxy(f'http://localhost:8000', allow_none=True)
    print(proxy.request(randint(0,100)))


threads = [Thread(target=testing) for _ in range(3)]

for thread in threads:
    thread.start()
