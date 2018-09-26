from struct import Struct, calcsize

TYPE_REQUEST_APPENDENTRY = b'\x50'
TYPE_RESPONSE_APPENDENTRY = b'\x51'
TYPE_REQUEST_VOTE = b'\x56'
TYPE_RESPONSE_VOTE = b'\x57'
TYPE_DATAGRAM_FRAGMENT = b'\x2D'

TYPE_FIELD = 'c' # 1 byte
SERVER_ID_FEILD = '8s' # 8 bytes
TERM_FIELD = 'Q' # (8 bytes) unsigned long long  <-> integer
DATA_LENGTH_FIELD = 'H' # (2 bytes) unsigned short  <-> integer

BOOL_FIELD = '?' # (1 byte)  <-> bool
LOG_INDEX_FIELD = 'Q' # (8 bytes) unsigned long long  <-> integer


# type, serverid, term, datalength
dgarm_header_struct = Struct(
    '!' + TYPE_FIELD + SERVER_ID_FEILD + TERM_FIELD + DATA_LENGTH_FIELD
)

vote_request_body_struct = Struct('!' +LOG_INDEX_FIELD + LOG_INDEX_FIELD)

vote_response_body_struct = Struct('!' +BOOL_FIELD)

append_entry_body_struct = Struct('!' +LOG_INDEX_FIELD)


unpack_dgram_header = dgarm_header_struct.unpack_from
pack_dgram_header = dgarm_header_struct.pack

