from Client.app import App
import socket
from Middle.api import *

if __name__ == '__main__':
    HOST: str = "::1" # Loopback for now but will be changed later
    PORT: int = 5000
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # Connect
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Server Not working")
        exit(1)

    app = App(s)
    app.mainloop()

    # Testing
    # send(s, {"type": "Database", "query": {"type": "Update", "table": "cart", "content": {"name": "Paneer Tikka", "user": 9897198971}}})
    # print(recv(s))
    # print("sent 2nd")
    # send(s, {"type": "Otp", "number": "9897143925"})
    # print(recv(s))
    # send(s, {"type": "Database", "query": {"type": "Update", "table": "cart", "content": {"name": "Dahi Kebab", "user": 9897198971}}})
    # print(recv(s))
    # send(s, {"type": "Database", "query": {"type": "Read", "table": "cart", "content": ""}})
    # print(recv(s))
    # send(s, {"type": "Database", "query": {"type": "Delete", "table": "cart", "content": {"id": 2}}})
    # print(recv(s))
    send(s, {"type": "Close"})
    s.close()
