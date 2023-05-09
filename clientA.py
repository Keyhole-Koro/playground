import socket

HOST = ''
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Listening on {HOST}:{PORT}')

while True:
	client_socket, client_address = server_socket.accept()
	print(f'Connection from {client_address}')

	data = client_socket.recv(1024)
	print(f'Received: {data.decode()}')

	response = 'Hello, client!'.encode()
	client_socket.sendall(response)

	client_socket.close()
