import pickle
import struct

from utils import *

fname = "Network Functions"

def send_msg(sock, msg):
    msg = pickle.dumps(msg)
    msg = struct.pack('>I', len(msg)) + msg

    Utils.log(fname, "Sending message of length: " + str(len(msg)))

    sock.sendall(msg)

def recv_msg(sock):
    Utils.dlog(fname, "Waiting for message...")

    raw_msglen = recvall(sock, 4)

    Utils.dlog(fname, "Received message of length: " + raw_msglen)
    if not raw_msglen:
        return None
        Utils.dlog(fname, "Received nothing")

    msglen = struct.unpack('>I', raw_msglen)[0]
    Utils.dlog(fname, "Waiting for a message with " + str(msglen) + " bytes")

    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            return None

        data += packet

    # Utils.log(fname, data)
    data = pickle.loads(data)
    return data
