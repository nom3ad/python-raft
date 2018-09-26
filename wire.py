import struct

TYPE_REQUEST_APPENDENTRY = b'\x50'
TYPE_RESPONSE_APPENDENTRY = b'\x51'

TYPE_REQUEST_VOTE = b'\x56'
TYPE_RESPONSE_VOTE = b'\x57'

TYPE_DATAGRAM_FRAGMENT = b'\x2D'

LEN_TYPE_FIELD = 1
LEN_TERM = 1
LEN_SERVER_ID = 16
LEN_LOG_INDEX = 8
LEN_BOOL = 1
LEN_DATA_LENGTH = 1

LEN_HEARTBEAT_APPENDENTRY_PACKET = (LEN_TYPE_FIELD +
                                    LEN_TERM +
                                    LEN_SERVER_ID +
                                    LEN_LOG_INDEX +
                                    LEN_TERM +
                                    LEN_LOG_INDEX +
                                    LEN_DATA_LENGTH)

LEN_REQUEST_VOTE_PACKET = (LEN_TYPE_FIELD +
                           LEN_TERM +
                           LEN_SERVER_ID +
                           LEN_LOG_INDEX +
                           LEN_LOG_INDEX)

LEN_RESPONSE_VOTE_PACKET = (LEN_TYPE_FIELD +
                            LEN_TERM +
                            LEN_BOOL)
