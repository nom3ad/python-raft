from __future__ import print_function

from transport import BaseUDPTransport
import struct
from wire import *


class RaftUdpTransport(BaseUDPTransport):

    def handle(self, data, address):  # pylint:disable=method-hidden
        _type, server_id , term, data_len = unpack_dgram_header(data)

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
    print('starting raft udp transport on :9000')
    rt = RaftUdpTransport(':9000').serve_forever() # bloks
    # do whatever with rt
    
