import socket
import json
# from time import sleep

def send(s: socket.socket, obj: dict):
    objParsed = json.dumps(obj)
    s.sendall(objParsed.encode())
    # sleep(0.2)  # So that recv becomes buffered

def recv(s: socket.socket):
    obj = s.recv(2048)
    if not obj:
        return 0
    obj = obj.decode()
    # obj = obj[:-1].split('}')
    # obj = "},".join(obj)
    # obj = '[' + obj + ']'
    print(obj)
    objParsed = json.loads(obj)
    return objParsed
