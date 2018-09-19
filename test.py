from __future__ import print_function
from gevent.server import DatagramServer
import gevent
import struct
from wire import *

class EchoServer(DatagramServer):

    def handle(self, data, address):  # pylint:disable=method-hidden
        _type = data[0]
        if _typ == 
        self.socket.sendto(('Received %s bytes' % len(data)).encode('utf-8'), address)


if __name__ == '__main__':
    print('Receiving datagrams on :9000')
    EchoServer(':9000').serve_forever()
