
import socket
import select

class BaseUDPServer(object):
    max_dgarm_size_expected = 1024

    def __init__(self, address):
        self.socket = socket.socket( socket.AF_INET,
                                    socket.SOCK_DGRAM)
        addr, port = address.split(':')
        self.server_address = addr, int(port)
        self.break_flag = False
        self.write = self.socket.sendto

    def handle(self, data, addr):
        raise NotImplementedError

    def serve_forever(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

        while not self.break_flag:
            readable, writable, errored = select.select([self.socket], [], [],0.01)
            print readable, writable, errored 
            if readable:
                data, addr = self.socket.recvfrom(self.max_dgarm_size_expected)
                try:
                    self.handle(data, addr)
                except:
                    pass

    def close(self):
        self.break_flag = True
        self.socket.close()
