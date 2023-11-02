import socket
import json

def send(s: socket.socket, obj: dict):
    objParsed = json.dumps(obj)
    s.sendall(objParsed.encode())

def recv(s: socket.socket):
    obj = s.recv(4096)
    if not obj:
        return 0
    obj = obj.decode()
    # obj = obj[:-1].split('}')
    # obj = "},".join(obj)
    # obj = '[' + obj + ']'
    objParsed = json.loads(obj)
    return objParsed
