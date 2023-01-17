from xmlrpc.client import ServerProxy
from threading import Thread
from random import randint

def testing():
    i = randint(0,2)
    proxy = ServerProxy(f'http://localhost:800{i}')
    print(proxy.sendProposal())


threads = [Thread(target=testing) for _ in range(3)]

for thread in threads:
    thread.start()
