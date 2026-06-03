import socket
import json
import struct

def send_msg(sock, data: dict):
    payload = json.dumps(data).encode('utf-8')
    header = struct.pack('>I', len(payload))
    sock.sendall(header + payload)

def recv_msg(sock) -> dict | None:
    raw_len = _recv_exact(sock, 4)
    if raw_len is None:
        return None
    msg_len = struct.unpack('>I', raw_len)[0]
    raw_body = _recv_exact(sock, msg_len)
    if raw_body is None:
        return None
    return json.loads(raw_body.decode('utf-8'))

def _recv_exact(sock, n) -> bytes | None:
    buffer = b''
    while len(buffer) < n:
        try:
            chunk = sock.recv(n - len(buffer))
            if not chunk:
                return None
            buffer += chunk
        except:
            return None
    return buffer
