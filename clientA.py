import socket
import threading

def receive_message(sock):
	while True:
		data = sock.recv(1024)
		if not data:
			break
		print(f"Received: {data.decode()}")

def get_input(sock):
	while True:
		user_input = input()
		sock.sendall(user_input.encode())

server_address = ('localhost', 12345)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
sock.connect(server_address)

# Start the thread to receive messages
receive_thread = threading.Thread(target=receive_message, args=(sock,))
receive_thread.daemon = True
receive_thread.start()

# Start the thread to get input from the user and send messages
input_thread = threading.Thread(target=get_input, args=(sock,))
input_thread.daemon = True
input_thread.start()

# Wait for the input thread to complete (which will never happen)
input_thread.join()
