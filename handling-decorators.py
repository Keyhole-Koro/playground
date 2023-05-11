import tkinter as tk
import threading
import time
import socket

import p2p_communicate
client_socket = None
msgs = []

def get_input():
	global client_socket
	def handle_return(event):
		msg = entry.get()
		#opponentIP = opponent[0][0]
		#opponentPORT = opponent[0][1]
		#with p2p.p2pconnect_to(opponentIP, opponentPORT) as opponent:
		#	opponent.sendall(msg.encode())
		response = msg.encode()
		client_socket.sendall(response)
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
	HOST = ''
	PORT = 12345
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((HOST, PORT))
	server_socket.listen(1)

	print('listen')
	client_socket, client_address = server_socket.accept()

	print(f'Connection from {client_address}')

	data = client_socket.recv(1024)
	print(f'Received: {data.decode()}')

	#response = 'Hello, client!'.encode()
	#client_socket.sendall(response)
	#opponent.append(client_address)
	#client_socket.close()
		
thread1 = threading.Thread(target=get_input)
thread2 = threading.Thread(target=listen)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
