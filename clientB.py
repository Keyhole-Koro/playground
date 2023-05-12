import socket
import threading
import tkinter as tk

msgs = []
client_socket = None
def first_contact():
	global client_socket
	# IP address and port number of the listening computer
	ip_address = 'localhost'
	port = 12345

	# Create a client socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the listening computer
	client_socket.connect((ip_address, port))

	# Send data to the listening computer
	data = 'succesufull connection'
	client_socket.sendall(data.encode())

	# Receive data from the listening computer
	received_data = client_socket.recv(1024).decode()
	print(received_data)

first_contact()

def send():
	global client_socket
	def handle_return(event):
		msg = entry.get()
		response = msg.encode()
		client_socket.sendall(response)
		msgs.append(msg)
		entry.delete(0, tk.END)

	root = tk.Tk()

	label = tk.Label(root, text="BEnter your message:")
	label.pack()

	entry = tk.Entry(root)
	entry.pack()

	entry.bind('<Return>', handle_return)

	root.mainloop()

	return msgs

def listen():
	global client_socket
	data = client_socket.recv(1024)
	
	print(f'Received: {data.decode()}')
	while True:

		# Receive data from the client
		data = client_socket.recv(1024).decode()
		print(f'Received: {data}')

	#response = 'Hello, client!'.encode()
	#client_socket.sendall(response)
	#opponent.append(client_address)
	#client_socket.close()
		
thread1 = threading.Thread(target=send)
thread2 = threading.Thread(target=listen)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
