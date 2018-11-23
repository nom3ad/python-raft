


STATE_FOLLOWER = 'follower'
STATE_CANDIDATE = 'candidate'
STATE_LEADER = 'leader'
from threading import Event
from Queue import Queue

ELECTION_TIMEOUT_MILLIS = 500

class Server(object):
    def __init__(self, id=0, peers=0):
        self.state = STATE_FOLLOWER
        self.peers = peers
        self.log_idx=0
        self.term=0
        self.log_term=0
        self.node_dict={0:['127.0.0.1',8120,False],1:['127.0.0.1',8121,False],2:['127.0.0.1',8122,False]}

    def run(self):
        while True:
            pass

    def add_node_master(self, server_addr):
        for value in self.node_dict.itervalues():
            if (value[0],value[1])==server_addr and value[2]==False:  #node_list=[ip_addr,port,actv/de-actv]
                value[2]=True
            elif (value[0],value[1])!=server_addr:
                value[2]=False
            else:
                value[2]=True

        
# def when_timeout():
#     pass


    
