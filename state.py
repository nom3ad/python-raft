


STATE_FOLLOWER = 'follower'
STATE_CANDIDATE = 'candidate'
STATE_LEADER = 'leader'
from threading import Event

ELECTION_TIMEOUT_MILLIS = 500

class Server(object):
    def __init__(self, id=0, peers=0):
        self.state = STATE_FOLLOWER
        self.peers = peers
        self.log_idx=0
        self.term=0
        self.log_term=0
        self.node_dict={0:('127.0.0.1',8120,True),0:('127.0.0.1',9000,True)}

    def run(self):
        while True:
            pass

    def add_node(self, server_addr):
        for value in self.node_dict.itervalues():
            if value[0]==server_addr and value[2]==False:  #node_list=[ip_addr,port,actv/de-actv]
                value[2]=True
        
# def when_timeout():
#     pass


    
