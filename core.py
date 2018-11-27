from __future__ import print_function

from transport import BaseUDPTransport
import struct
from wire import *
from state import *
import array
import time
import sys
import threading
from smp_http import *



vote_count=1    #my own vote

def on_append_entry_recieved(leader_id, term, prev_log_idx,
                             prev_log_term, commit_idx, payload):
    pass

# server_obj=Server()
def on_vote_recieved(*k):
    global vote_count
    vote_count+=1
    print("Elected as leader")
    # if vote_count > peer_count/2:
        

        
def on_vote_request(cand_term,curr_term,cand_log_term,curr_log_term,cand_log_idx,curr_log_idx):
    if cand_term>curr_term and cand_log_idx>=curr_log_idx and cand_log_term>=curr_log_term:
        return True
    else:
        return False

class PartialAppendEntry:
    def __init__(self, dg_count):
        self.payloads = [None] * dg_count

    def add_first_segment(self, leader_id, term, prev_log_idx,
                          prev_log_term, commit_idx, payload):
        self.leader_id = leader_id
        self.term = term
        self.prev_log_idx = prev_log_idx
        self.prev_log_term = prev_log_term
        self.commit_idx = commit_idx
        self.payloads[0] = payload
        return all(self.payloads)

    def add_partial_segment(self, index, payload):
        self.payloads[index] = payload
        return all(self.payloads)

    def club_payloads(self):
        return b''.join(self.payloads)


fragmented_map = {}


class RaftUdpTransport(BaseUDPTransport):

    # def __init__(self, address, raft_engine):
    #     self.raft_engine = raft_engine
   
            #print(nodes[0],nodes[1])
    # @property
    # def node_dict(self):
    #     return self.node_dict
    # @node_dict.setter
    # def node_dict(self, v)
    #     reqhand.nodes=v
    #     self.node_dict = v

    def datagram_received(self, data, address):  # pylint:disable=method-hidden
        log_json = []
        f = open("log.json", "a")
        #print('header broke?')
        _type, server_id, term = unpack_dgram_header(data)
        # assert data_len == len(data)
        if _type == TYPE_DATAGRAM_FRAGMENT:
            print('data frag broke?')
            dg_count, dg_id, dg_index = unpack_fragment_struct(data)
            payload = data[FRAGMENTED_DG_PREAMBLE_SZ:]
            pae = fragmented_map.get(dg_id, PartialAppendEntry(dg_count))
            if pae.add_partial_segment(dg_index, payload):
                fragmented_map.pop(dg_id, None)
                on_append_entry_recieved(server_id, term,
                                         pae.prev_log_idx,
                                         pae.prev_log_term,
                                         pae.commit_idx,
                                         pae.club_payloads())

        elif _type == TYPE_REQUEST_VOTE:
            print('On vote req')
            cand_log_idx,cand_log_term = unpack_vote_request_struct(data)
            h = pack_dgram_header(TYPE_RESPONSE_VOTE,'10',self.my.term)
            print(term)
            print(self.my.term)
            if on_vote_request(term,self.my.term,cand_log_term,self.my.log_term,cand_log_idx,self.my.log_idx):
                response = True
                b = pack_vote_response_struct(response)
                self.my.term=term
                self.my.state=STATE_FOLLOWER
                
            else:
                response = False
                b = pack_vote_response_struct(response)
                
            #print(address)
            self.write(h+b,address)
            return response

        elif _type == TYPE_RESPONSE_VOTE:
            print('On vote rec')
            (voted,) = unpack_vote_response_struct(data,)
            print(voted)
            if voted:
                self.peers_voted+=1
                if self.peers_voted >= int(self.my.peers/2):
                    self.my.state = STATE_LEADER
                    self.my.add_node_master(self.server_address)
                on_vote_recieved(server_id, term, voted)
            else:
                self.my.term-=1
                print('votereq fal',self.my.term)

        elif _type == TYPE_REQUEST_APPENDENTRY:
            print('req_app broke?')
            (prev_log_idx, prev_log_term,
             commit_idx, dg_count, dg_id) = unpack_appendentry_request_struct(data)
            payload = data[APPEND_ENTRY_PREAMBLE_SZ:]

            if dg_count == 0:
                on_append_entry_recieved(server_id, term, prev_log_idx,
                                         prev_log_term, commit_idx, payload)
            else:
                pae = fragmented_map.get(dg_id, PartialAppendEntry(dg_count))
                if pae.add_first_segment(server_id, term, prev_log_idx,
                                         prev_log_term, commit_idx, payload):
                    fragmented_map.pop(dg_id, None)
                    on_append_entry_recieved(server_id, term, prev_log_idx,
                                             prev_log_term, 
                                             commit_idx, pae.club_payloads())

        elif _type == TYPE_RESPONSE_APPENDENTRY:
            pass
        elif _type == TYPE_HB:
            #print('HB broke?')
            bt = unpack_heartbeat_struct(data)
#            print("HB "+str(bt))
            #print(address)
            self.my.add_node_master(address)

        elif _type == TYPE_WB_DATA:
            a = time.time()
            print(a)
            wb_req, = unpack_wb_struct(data)
            temp = wb_req.replace('\\x00','')
            log_json.append([temp,self.my.term])
            #f.write(log_json)
            print(temp,log_json)
            print(time.time() - a)
            return False
        else:
            #print(time.time())
            self.write(data, address)
            # print(address)
            raise ValueError("unknown type")

        return True


if __name__ == '__main__':
    print('starting raft udp transport on :'+sys.argv[1])
    
    time.sleep(1)

    try:
        rt = RaftUdpTransport('127.0.0.1:'+sys.argv[1])
    # rt.register_timeoyt(10, when_timeout)
    # rt.register_timeoyt(60, on_evey_minute)
       # pdb.set_trace()
        ab=threading.Thread(target=ak,args=(sys.argv[2],rt))
        ab.start()
        rt.serve_forever()  # blocks

    # do whatever with rt
    except Exception as e:
        print('Exception here',e)
        raise
        #rt.close()

    
    