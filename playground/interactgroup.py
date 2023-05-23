import tkinter as tk
import threading
import socket

import p2p_communicate

client_info = {'Keyhole': ('localhost', 42345), 'Kamina': ('localhost', 49000), 'kjavik': ('localhost', 48000)}
client_socket = None
left_msg = None

def connect(client_name):
	global client_socket
	ip_address, port = client_info['Keyhole']
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((ip_address, port))
		print('Successful connection')
		data = f'{client_name} Successful connection'
		client_socket.sendall(data.encode())
	except Exception as e:
		print('Error connecting to client:', e)


def send(user):
	global client_socket
	def handle_return(event):
		msg = entry.get()
		if client_socket is None:
			try:
				connect(msg)
			except Exception as e:
				print('Error not found opponent:', e)
		else:
			try:
				response = (f'{user} : {msg}').encode()
				client_socket.sendall(response)
				print(f'{user} : {msg}')
			except Exception as e:
				print('Error sending message:', e)
		entry.delete(0, tk.END)

	root = tk.Tk()
	label = tk.Label(root, text=f"{user} : Enter your message:")
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


def listening(client_name):
	global left_msg
	ip_address, port = client_info[client_name]
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ip_address, port))
	server_socket.listen()
	client_socket, client_address = server_socket.accept()
	while True:
		try:
			data = client_socket.recv(1024).decode()
			left_msg = data
			print('left_msg', left_msg)
			#print(data)
		except Exception:
				pass
			
#doesnt work

def as_server():
	client = ['Keyhole', 'Kamina', 'kjavik']
	for c in range(len(client)):
		thread_listening = threading.Thread(target=listening, args=(client[c],))
		thread_listening.start()
		thread_listening.join()

def display_message():
	global left_msg
	while True:
		if left_msg is not None:
			print(left_msg)
			left_msg = None
		else:
			pass

if __name__ == '__main__':
	while True:
		user = input('Enter your name:')
		if user in client_info:
			break
		else:
			print('Client not found')

	if user == 'Keyhole':
		as_server_thread = threading.Thread(target=as_server)
		as_server_thread.start()
	else:
		connect(user)
		listening_thread = threading.Thread(target=listening, args=(user,))
		listening_thread.start()

	send_thread = threading.Thread(target=send, args=(user,))
	display_message_thread = threading.Thread(target=display_message)
	
	send_thread.start()
	display_message_thread.start()
	
	send_thread.join()
	display_message_thread.join()
	
	if user == 'Keyhole':
		as_server_thread.join()
	else:
		listening_thread.join()
