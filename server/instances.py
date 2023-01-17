from random import randint
from xmlrpc.client import ServerProxy 
from threadWithReturn import ThreadReturn
from promise import Promise
INSTANCES = [f'http://localhost:{8000}', f'http://localhost:{8001}', f'http://localhost:{8001}']

'''
    Paxos Algorithm
'''
class Paxos:
    def __init__(self) -> None:
        self.currentIdentifier = -1
        self.greatestPromise = 0
        pass

    def generateIdentifier(self):
        return self.currentIdentifier + randint(1,3)

    # This function should be called in a thread 
    def sendPrepareToInstance(self, otherInstance):
        id, instance = otherInstance

        identifier = self.generateIdentifier()
        # This is a rpc call
        response = instance.promise(identifier)

        print(f"Instance {id}")

        return response



    def promise(self, identifier):
        if identifier >= self.greatestPromise:
            self.greatestPromise = identifier
             
        pass



'''
    Instance Class
'''
class Instance(Paxos):
    def __init__(self, port) -> None:
        Paxos.__init__()
        # RPCs related variables
        self.localPort = port
        self.localAddress = f'http://localhost:{port}'
        self.instances = {}

        self.INSTANCE_TIMEOUT = 3

        pass

    def connectToInstances(self) -> None:
        for INSTANCE in INSTANCES:
            if INSTANCE != self.localAddress:
                try:
                    self.instances[INSTANCE] = ServerProxy(INSTANCE, allow_none=True)
                except:
                    print('Not able to connect to some instances')
        print('Connected to other instances')


    def request(self, number):
        self.connectToInstances()
        
        # Sending a promise request to each unstance
        threads = [ThreadReturn(target=self.sendPrepareToInstance, args=[(id,instance)]) for id, instance in self.instances.items()]
        # 
        for t in threads: t.start()

        responses = [t.join(self.INSTANCE_TIMEOUT) for t in threads]


        pass



