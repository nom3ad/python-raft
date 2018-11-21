from __future__ import print_function
from struct import Struct, calcsize
from functools import partial

TYPE_REQUEST_APPENDENTRY = b'\x50'
TYPE_RESPONSE_APPENDENTRY = b'\x51'
TYPE_REQUEST_VOTE = b'\x56'
TYPE_RESPONSE_VOTE = b'\x57'
TYPE_DATAGRAM_FRAGMENT = b'\x2D'
TYPE_HB = b'\x40'

TYPE_FIELD = 'c'  # 1 byte
SERVER_ID_FEILD = '8s'  # 8 bytes
TERM_FIELD = 'Q'  # (8 bytes) unsigned long long  <-> integer

BOOL_FIELD = '?'  # (1 byte)  <-> bool
LOG_INDEX_FIELD = 'Q'  # (8 bytes) unsigned long long  <-> integer
LOG_INDEX_TERM= 'Q'  # (8 bytes) unsigned long long  <-> integer

HB = '8s'
# appendentry_data_seg
DG_ID_FIELD = '8s'
DG_COUNT_FEILD = 'H'
DG_INDEX_FEILD = DG_COUNT_FEILD    # unsigned char  1 Byte <> int

# type, serverid, term, datalength
dgarm_header_struct = Struct(
    '!' + TYPE_FIELD + SERVER_ID_FEILD + TERM_FIELD
)

vote_request_struct = Struct('!' + LOG_INDEX_FIELD + LOG_INDEX_TERM)
vote_response_struct = Struct('!' + BOOL_FIELD)

heartbeat_struct=Struct(
    '!' + HB)
append_entry_struct = Struct(
    '!' + LOG_INDEX_FIELD + TERM_FIELD + LOG_INDEX_FIELD + DG_COUNT_FEILD + DG_ID_FIELD)

fragment_struct = Struct('!' + DG_COUNT_FEILD +  DG_ID_FIELD + DG_INDEX_FEILD)

DGRAM_HEADER_SZ = dgarm_header_struct.size 
MAX_APPENDABLE_DG_COUNT = 256**calcsize(DG_COUNT_FEILD) - 1
MAX_DGRAM_SIZE = 1024
MAX_DG_PAYLOAD_SIZE = MAX_DGRAM_SIZE - (DGRAM_HEADER_SZ +
                                        max(append_entry_struct.size,
                                            vote_request_struct.size,
                                            vote_response_struct.size,
                                            fragment_struct.size)
                                        )


APPEND_ENTRY_PREAMBLE_SZ = DGRAM_HEADER_SZ + append_entry_struct.size
FRAGMENTED_DG_PREAMBLE_SZ = DGRAM_HEADER_SZ + fragment_struct.size

MAX_APPENDENTRY_SIZE = MAX_DG_PAYLOAD_SIZE * MAX_APPENDABLE_DG_COUNT

print ("MAX_DG_PAYLOAD_SIZE:",MAX_DG_PAYLOAD_SIZE)
print ("MAX_APPENDABLE_DG_COUNT:",MAX_APPENDABLE_DG_COUNT)
print ("MAX_APPENDENTRY_SIZE:",MAX_APPENDENTRY_SIZE/1024, 'KB')


unpack_dgram_header = dgarm_header_struct.unpack_from
pack_dgram_header = dgarm_header_struct.pack
pack_vote_response_struct = vote_response_struct.pack
pack_vote_request_struct = vote_request_struct.pack
pack_heartbeat_struct = heartbeat_struct.pack

unpack_heartbeat_struct= partial(heartbeat_struct.unpack_from,offset = DGRAM_HEADER_SZ)
unpack_vote_request_struct = partial(vote_request_struct.unpack_from, offset=DGRAM_HEADER_SZ)
unpack_vote_response_struct = partial(vote_response_struct.unpack_from, offset=DGRAM_HEADER_SZ)
unpack_appendentry_request_struct = partial(append_entry_struct.unpack_from, offset=DGRAM_HEADER_SZ)
unpack_fragment_struct = partial(fragment_struct.unpack_from, offset=DGRAM_HEADER_SZ)



