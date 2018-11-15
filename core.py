from __future__ import print_function

from transport import BaseUDPTransport
import struct
from wire import *
import array


def on_append_entry_recieved(leader_id, term, prev_log_idx,
                             prev_log_term, commit_idx, payload):
    pass

def on_vote_recieved(*k):pass

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

    def datagram_received(self, data, address):  # pylint:disable=method-hidden
        _type, server_id, term = unpack_dgram_header(data)
        # assert data_len == len(data)
        if _type == TYPE_DATAGRAM_FRAGMENT:
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
            pass

        elif _type == TYPE_RESPONSE_VOTE:
            (voted,) = unpack_vote_response_struct(data)
            on_vote_recieved(server_id, term, voted)

        elif _type == TYPE_REQUEST_APPENDENTRY:
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
                                             prev_log_term, commit_idx, pae.club_payloads())

        elif _type == TYPE_RESPONSE_APPENDENTRY:
            pass

        else:
            self.write(data, address)
            raise ValueError("unknown type")


if __name__ == '__main__':
    print('starting raft udp transport on :9000')
    rt = RaftUdpTransport(':9000').serve_forever()  # bloks
    # do whatever with rt
