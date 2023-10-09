import socket
from Middle.api import *
from Server.handle_req import handle

HOST = "::1"
PORT = 5000

s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# db

# Bind
s.bind((HOST, PORT))

# Listen
s.listen()

# Accept
connection, address = s.accept()

with connection:
	print(f"Connection mili gawa {address}")
	while True:
		data = recv(connection)
		if data == -1:
			break
		elif data != 0:
			if handle(data) == -1:
				send(connection, "Invalid")
			else:
				print(type(data), data)
				send(connection, data)

s.close()
