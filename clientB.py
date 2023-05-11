import socket

# IP address and port number of the listening computer
ip_address = 'localhost'
port = 12345

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the listening computer
client_socket.connect((ip_address, port))

# Send data to the listening computer
data = 'Hello, world!'
client_socket.sendall(data.encode())

# Receive data from the listening computer
received_data = client_socket.recv(1024).decode()
print(received_data)
