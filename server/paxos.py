from random import randint
from xmlrpc.client import ServerProxy 
from threadWithReturn import ThreadReturn

PORTS = [8000, 8001, 8002]


class Paxos:
    def __init__(self, port) -> None:
        # RPCs related variables
        self.localPort = port

        # Paxos related variables
        self.currentProposalNumber= -1
        self.currentValue = None
        self.latestProposal = -1
        self.latestValue = None

        # Connecting to all other instances
        self.instances = [ServerProxy((f'http://localhost:{port}')) for port in PORTS if port != self.localPort]

        pass

    def sendProposal(self):
        promises = [] # An array that stores the responses of the values recived

        # Generate new proposal number
        proposalNumber = self.currentProposalNumber + randint(1,3)

        # Send porposal in thread
        threads = [ThreadReturn(target=instance.prepare, args=[proposalNumber]) for instance in self.instances]

        for thread in threads:
            thread.start()

        for thread in threads:  
            # Giving each thread 2 second to responde
            promises.append(thread.join(3))
        
        '''
            Counting the proposals recieved
        '''
        print(f"Promises recieved: {promises}")
        for response in promises:
            if response:
                promise, latestProposal, latestValue = response
                if promise:
                    if latestProposal > self.latestProposal:
                        # Stop the function here because our proposal is behind
                        # Update the new values for latest proposal
                        self.latestValue = latestValue
                        self.latestProposal = latestProposal
                        
                    else:
                        # This is the good way, when everythong goes well and machines do not fail
                        # Choose the value to be selected and send it to the other instances.
                        # ... Write code only here in this function
                        return True

        # Try again with another proposal number.
        return False

    
    def prepare(self, n):

        print(f'Proposal {n} Recieved')

        promise = False
        if n > self.latestProposal: 
            promise = True
            self.latestProposal = n

        print(f"Responding with promise: {promise}")

        return promise, self.latestProposal, self.latestValue
