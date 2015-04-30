import pickle
import struct

from utils import *

fname = "Network Functions"

def send_msg(sock, msg):
    msg = pickle.dumps(msg)
    msg = struct.pack('>I', len(msg)) + msg

    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)

    if not raw_msglen:
        return None

    msglen = struct.unpack('>I', raw_msglen)[0]

    contents = recvall(sock, msglen)
    contents = pickle.loads(contents)
    return contents

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            return None

        data += packet

    return data
