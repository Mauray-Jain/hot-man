from Client.app import App
import socket
from Middle.api import *

if __name__ == '__main__':
    HOST: str = "::1" # Loopback for now but will be changed later
    PORT: int = 5000
    s: socket.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # Connect
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Server Not working")
        exit(1)

    app = App()
    app.mainloop()

    s.close()
