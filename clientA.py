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
	if client_name in l_ip_address and client_name in l_port:
		ip_address = l_ip_address[client_name]
		port = l_port[client_name]
		try:
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_socket.connect((ip_address, port))
			data = 'succesufull connection'
			print(data)
			client_socket.sendall(data.encode())
			received_data = client_socket.recv(1024).decode()
			print(received_data)
		except Exception as e:
			print('Error connecting to client:', e)
	else:
		print('Client not found.')

def send():
	global client_socket
	def handle_return(event):
		msg = entry.get()
		if client_socket is None:
			try:
				first_contact(msg)
				label = tk.Label(root, text="Enter your message:")
			except Exception as e:
				print('Error not found opponent:', e)
		else:
			try:
				response = msg.encode()
				client_socket.sendall(response)
				print('you:', msg)
				msgs.append(msg)
			except Exception as e:
				print('Error sending message:', e)
		entry.delete(0, tk.END)

	root = tk.Tk()

	label = tk.Label(root, text="Enter opponent name:")
	label.pack()

	entry = tk.Entry(root)
	entry.pack()

	entry.bind('<Return>', handle_return)

	root.mainloop()

	return msgs

def listen():
	global client_socket
	your_name = ''
	while True:
		your_name = input('Tell me your name in advance: ')
		if your_name in l_ip_address and your_name in l_port:
			break
		else:
			print("Error: Invalid name.")
	
	y_ip_address = l_ip_address[your_name]
	y_port = l_port[your_name]

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((y_ip_address, y_port))
	server_socket.listen()

	client_socket, client_address = server_socket.accept()
	print(f'Connection from {client_address}')

	while True:
		data = client_socket.recv(1024).decode()
		print('opponent:', data)


thread1 = threading.Thread(target=send)
thread2 = threading.Thread(target=listen)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
