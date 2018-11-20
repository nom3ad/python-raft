
import socket
import select
import time
from wire import *
from state import *
import random
import threading
time_out=random.randint(4,7)


    


class BaseUDPTransport(object):
    max_dgarm_size_expected = 1024

    def __init__(self, address):
        self.socket = socket.socket( socket.AF_INET,
                                    socket.SOCK_DGRAM)
        addr,port = address.split(':')
        self.server_address = addr, int(port)
        self.break_flag = False
        self.write = self.socket.sendto
        self.my=Server()
            
    def send_dat():
        with lock:
            i=0
            i+=i
            h = pack_dgram_header(TYPE_REQUEST_APPENDENTRY,13,self.my.term)
            b = pack_heartbeat_struct('Beating '+i)
            for node in self.my.node_dict.itervalues():
                if self.server_address != (node[0],node[1]):
                    # print("Call ele1",(node[0],node[1]),self.server_address) 
                    self.write(h+b,(node[0],node[1]))
    
    def call_election(self):
        print("Call ele",self.my.term)
        h=pack_dgram_header(TYPE_REQUEST_VOTE,self.server_address[0],self.my.term)
        b=pack_vote_request_struct(self.my.term,self.my.log_idx)
        for node in self.my.node_dict.itervalues(): 
            if self.server_address != (node[0],node[1]):
                print("Call ele1",(node[0],node[1]),self.server_address) 
                self.write(h+b,(node[0],node[1]))
    
    def datagram_received(self, data, addr):
        raise NotImplementedError

    def serve_forever(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        sender = threading.Thread(target=send_dat,args=(,))
        sender.start()
        last_timeout = time.time()
        while not self.break_flag:
            
            if (time.time()-last_timeout)> time_out:
                if self.my.state == STATE_LEADER:
                    lock.set()              #If we dont add a thread we wont recieve the
                else:                       #response of the append entries
                    last_timeout = time.time()
                    self.my.term += 1     #Calling election increments the candidate term
                    self.call_election()
                    self.my.state = STATE_CANDIDATE    
                    print "TIME_OUT"
            readable, writable, errored = select.select([self.socket], [], [],0.01)
            if readable:
                data, addr = self.socket.recvfrom(self.max_dgarm_size_expected)
                print('transp',addr)
                last_timeout = time.time()
                    
                self.datagram_received(data, addr)
                    
                # except NotImplementedError:
                #     raise
                # except Exception as oops:
                #     # print(self.server_address)
                #     print("unhandled error on dg rcv:", oops)
    
    
    def close(self):
        self.break_flag = True
        self.socket.close()

