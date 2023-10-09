import socket
import json

def send(s: socket.socket, obj: dict) -> None:
    objParsed = json.dumps(obj)
    s.sendall(objParsed.encode())
    

def recv(s: socket.socket) -> dict | int:
    obj = s.recv(1024)
    if not obj:
        return 0
    objParsed = json.loads(obj.decode())
    if objParsed["type"] == "Close":
        return -1
    return objParsed
