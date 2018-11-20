import socket
from wire import *
import select

sock = socket.socket( socket.AF_INET,
                            socket.SOCK_DGRAM)



sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8120))
h=pack_dgram_header('2', 'abcd', 10010 )
b=pack_vote_request_struct(100,101)
#sock.sendto( h, ('', 9000),)
# sock.sendto( "asasas", ('', 9000),)
while True:
    
    readable, writable, errored = select.select([sock], [], [],0.01)
    if readable:    
        data,addr = sock.recvfrom(1024)      
        a,b=unpack_vote_request_struct(data)
        print repr(a+b)  
