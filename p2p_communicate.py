import socket

class p2pconnect_to:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.client_socket = None
	def __enter__(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (self.ip, self.port)
		self.client_socket.connect(server_address)
		print('Connected to server:', server_address)
		return self.client_socket
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.client_socket.close()
	
