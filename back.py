import socket
import selectors
import types
from Middle.api import *
from Server.handle_req import handle

HOST = "::1"
PORT = 5000

selector = selectors.DefaultSelector()
# db

# Accept
def accept_connection(s):
    connection, address = s.accept()
    print(f"Connection mili gawa {address}")
    s.setblocking(False)
    data = types.SimpleNamespace(addr = address, inb = b"", outb = b"")
    eventMask = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(connection, eventMask, data = data)

# with connection:
#     while True:
#         data = recv(connection)
#         if data == -1:
#             break
#         elif data != 0:
#             if handle(data) == -1:
#                 send(connection, {"status": "Invalid"})
#             else:
#                 print(type(data), data)
#                 send(connection, data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: # Ready to read
        recv_data = recv(sock)
        if recv_data != 0:
            for i in recv_data:
                if i["type"] == "Close":
                    print(f"Closing connection to {data.addr}")
                    selector.unregister(sock)
                    sock.close()
                    break
                print(i)
    if mask & selectors.EVENT_WRITE:  # Ready to write
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sock.sendall(data.outb)

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print(f"Sun raha hai na tu ro raha hoon main at {HOST} and {PORT}")
s.setblocking(False)
selector.register(s, selectors.EVENT_READ, data=None)

try:
    while True:
        events = selector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_connection(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Buhbye")
finally:
    selector.close()
