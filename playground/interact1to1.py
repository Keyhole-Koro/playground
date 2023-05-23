import tkinter as tk
import threading
import socket

import p2p_communicate

client_info = {'Keyhole': ('localhost', 12345), 'Kamina': ('localhost', 19000)}
client_socket = None
def first_contact(client_name):
	global client_socket
	if client_name in client_info:
		ip_address, port = client_info[client_name]
		try:
			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			client_socket.connect((ip_address, port))
			print('Successful connection')
			data = 'Successful connection'
			client_socket.sendall(data.encode())
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
			except Exception as e:
				print('Error not found opponent:', e)
		else:
			try:
				response = msg.encode()
				client_socket.sendall(response)
				print('You:', msg)
			except Exception as e:
				print('Error sending message:', e)
		entry.delete(0, tk.END)

	root = tk.Tk()
	label = tk.Label(root, text="Enter your message:")
	label.pack()
	entry = tk.Entry(root)
	entry.pack()
	entry.bind('<Return>', handle_return)
	root.mainloop()

def first_listen():
	global client_socket
	your_name = input('Tell me your name in advance: ')
	if your_name in client_info:
		y_ip_address, y_port = client_info[your_name]
	else:
		print('Invalid name')
		return
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((y_ip_address, y_port))
	server_socket.listen()
	client_socket, client_address = server_socket.accept()
	print(f'Connection from {client_address}')


def listening():
	global client_socket
	while True:
		try:
			data = client_socket.recv(1024).decode()
			print('opponent:', data)
		except Exception:
				pass
thread1 = threading.Thread(target=send)
thread2 = threading.Thread(target=first_listen)
listening = threading.Thread(target=listening)

thread1.start()
thread2.start()
listening.start()

thread1.join()
thread2.join()
listening.join()
