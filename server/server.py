from xmlrpc.server import SimpleXMLRPCServer
from instances import Instance
from socketserver import ThreadingMixIn
import socket
from threading import Thread

# Making SimpleXMLRPCServer a threaded version of the original
class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class Server():
    def __init__(self):
        self.IP = "localhost"
        self.PORT = 8000
        self.local = None


    def getAddres(self):
        return (self.IP, self.PORT)


    def findOpenPort(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(self.getAddres()) == 0


    def run(self):

        print(f'Looking for open port...')
        while self.findOpenPort():
            self.PORT += 1

        try:
            self.local = SimpleThreadedXMLRPCServer(self.getAddres(), allow_none=True)
            self.local.register_function(Instance(self.getAddres()[1]))

            print(f'Server running @ {self.getAddres()}')
            self.local.serve_forever()

        except KeyboardInterrupt:
            print('\nServer interrupted')


if __name__ == "__main__":
    s = Server()
    s.run()