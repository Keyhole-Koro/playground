import tkinter as tk
import threading
import time
import socket

import p2p_communicate
client_socket = None
msgs = []

def send():
	global client_socket
	def handle_return(event):
		msg = entry.get()
		response = msg.encode()
		client_socket.sendall(response)
		msgs.append(msg)
		entry.delete(0, tk.END)

	root = tk.Tk()

	label = tk.Label(root, text="AEnter your message:")
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
		
thread1 = threading.Thread(target=send)
thread2 = threading.Thread(target=listen)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
