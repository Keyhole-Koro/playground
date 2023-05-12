import tkinter as tk
import threading
import time
import socket

import p2p_communicate
client_socket = None
msgs = []
l_ip_address = {'Keyhole':'localhost', 'Kamina':'localhost'}
l_port = {'Keyhole':12345, 'Kamina':19000}

def first_contact(client_name):
	global client_socket
	ip_address = l_ip_address[client_name]
	port = l_port[client_name]
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		client_socket.connect((ip_address, port))
		
		data = 'succesufull connection'
		
		client_socket.sendall(data.encode())
		
		received_data = client_socket.recv(1024).decode()
		print(received_data)
	except clientNotFound:
		print('client not found')

def send():
	global client_socket
	def handle_return(event):
		msg = entry.get()
		if client_socket == None:
			first_contact(msg)
		else:
			response = msg.encode()
			client_socket.sendall(response)
			print(msg)
			msgs.append(msg)
		entry.delete(0, tk.END)

	root = tk.Tk()

	label = tk.Label(root, text="Enter your message:")
	label.pack()

	entry = tk.Entry(root)
	entry.pack()

	entry.bind('<Return>', handle_return)

	root.mainloop()

	return msgs

def listen():
	global client_socket
	HOST = 'localhost'
	PORT = 12345
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen()
	
	client_socket, client_address = server_socket.accept()
	print(f'Connection from {client_address}')
		
	while True:

		# Receive data from the client
		data = client_socket.recv(1024).decode()
		print(f'Received: {data}')

		# Send a response back to the client
		#client_socket.sendall(data.encode())
		#print(f"Sent: {data}")

		# Close the client socket
		#client_socket.close()
def message_log():
	print(msg)

thread1 = threading.Thread(target=send)
thread2 = threading.Thread(target=listen)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
