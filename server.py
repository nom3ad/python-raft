from __future__ import print_function

from udpserver import BaseUDPServer
import struct
from wire import *


class RaftUdpServer(BaseUDPServer):

    def handle(self, data, address):  # pylint:disable=method-hidden
        _type = data[0]
        if _type == TYPE_DATAGRAM_FRAGMENT:
            pass

        elif _type == TYPE_REQUEST_VOTE:
            pass

        elif _type == TYPE_RESPONSE_VOTE:
            pass

        elif _type == TYPE_REQUEST_APPENDENTRY:
            pass

        elif _type == TYPE_RESPONSE_APPENDENTRY:
            pass

        else:
            self.write(data, address)
            raise ValueError("unknown type")

if __name__ == '__main__':
    print('starting raft udp server on :9000')
    RaftUdpServer(':9000').serve_forever()
