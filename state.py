


STATE_FOLLOWER = 'follower'
STATE_CANDIDATE = 'follower'
STATE_LEADER = 'follower'
from threading import Event

ELECTION_TIMEOUT_MILLIS = 500

class Server(object):
    def __init__(self, id, peers):
        self.state = STATE_FOLLOWER
        self.peers = peers

    def run(self):
        while True:
            if


    
