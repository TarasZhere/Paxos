from xmlrpc.server import SimpleXMLRPCServer
from paxos import Paxos
from socketserver import ThreadingMixIn
from socket import socket

# Making SimpleXMLRPCServer a threaded version of the original
class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Server():
    def __init__(self):
        self.addr = ("localhost", 8000)
        self.IP = "localhost"
        self.PORT = 8000
        self.local = None

    def getAddres(self):
        return self.IP,self.PORT

    def findOpenPort(self):
        with socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            return s.connect_ex(self.getAddres()) == 0


    def run(self):

        print(f'Lookng for open port...')
        while self.findOpenPort():
            self.PORT += 1
            pass

        try:
            self.local = SimpleThreadedXMLRPCServer(self.addr, allow_none=True)
            self.local.register_instance(Paxos(self.getAddres()))

            self.local.serve_forever()

        except KeyboardInterrupt:
            print('\nServer was stopped')

if __name__ == "__main__":
    s = Server()
    s.run()