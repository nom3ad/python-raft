import socket
from wire import *
sock = socket.socket( socket.AF_INET,
                            socket.SOCK_DGRAM)



sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8999))
pack_dgram_header(TYPE_REQUEST_VOTE, 'abcd', 10010, 187 )

sock.sendto( pack_dgram_header(TYPE_REQUEST_VOTE, 'abcd', 10010, 187 ) , ('', 9000),)