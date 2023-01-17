from xmlrpc.server import SimpleXMLRPCServer
from paxos import Paxos
from socketserver import ThreadingMixIn

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Server():
    addr = ("localhost",8000)
    def __init__(self):

        while True:
            try:
                self.local = SimpleThreadedXMLRPCServer(self.addr)
                break
            except:
                self.addr = self.addr[0], self.addr[1] + 1 
                print(f'Updating port to {self.addr[1]}')

        self.local.register_instance(Paxos(self.addr[1]))

    def run(self):
        try:
            print(f'Server is running at {self.addr}...')
            self.local.serve_forever()
        except KeyboardInterrupt:
            print('\nServer has been stopped')

if __name__ == "__main__":
    s=Server()
    s.run()