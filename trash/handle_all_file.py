import tkinter as tk
import threading
import socket

import blockchain
import p2p_communicate as p2p

user_info = [
	('user1', ('localhost', 42345)),
	('user2', ('localhost', 49000)),
	('user3', ('localhost', 48000)),
	('user4', ('localhost', 43345)),
	('user5', ('localhost', 44345)),
	('user6', ('localhost', 45345)),
	('user7', ('localhost', 46345)),
	('user8', ('localhost', 47345)),
	('user9', ('localhost', 48345)),
	('user10', ('localhost', 49345))
]

bc = blockchain.Blockchain()

def send_data(opponent_name, data, sender_name):
	try:
		if opponent_name in user_info:
			op_ip, op_port = user_info[opponent_name]
			with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
				if data.suffix:
					with open(data, 'rb') as file:
						file_data = file.read()
						op_socket.sendall(file_data)
				op_socket.sendall(data.encode())
		else:
			print(f"Opponent '{opponent_name}' does not exist in user_info.")
	except KeyError:
		print(f"Opponent '{opponent_name}' does not exist in user_info.")
	except Exception as e:
		print('Error:', e)

def look_for_file():
	

def sprinkle_files(data):
	chunk_size = 10000
	chunks = divide_into_chunks(data, chunk_size)
	for chunk in chunks:
		send_data
		

def divide_into_chunks(data, chunk_size):
	chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
	return chunks

def listening(client_name):
	ip_address, port = user_info[client_name]
	receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	receive_socket.bind((ip_address, port))
	receive_socket.listen()
	while True:
		try:
			client_socket, client_address = receive_socket.accept()
			for name, address in user_info.items():
				if address == client_address:
					client_name = name
					break
			data = client_socket.recv(10000).decode()
			if data.suffix:
				
			else:
				print(client_name, ':', data)
		except Exception:
				pass

def get_input(user):
	global user_info
	def handle_return(event):
		msg = entry.get()
		if ':' in msg:
			message = msg.split(":")
			opponent_name = message[0]
			data = message[1]
			if opponent_name in user_info:
				send_data(opponent_name, data, user)
			elif opponent_name == 'all':
				for client in user_info.keys():
					if client != user:
						send_data(client, data, user)
					else:
						pass
			else:
				print('user Not Found')
		else:
			print('invalid format')
		entry.delete(0, tk.END)

	root = tk.Tk()

	label = tk.Label(root, text="Enter your message:")
	label.pack()

	entry = tk.Entry(root)
	entry.pack()

	entry.bind('<Return>', handle_return)

	root.mainloop()

if __name__ == '__main__':
	while True:
		user = input('Enter your name:')
		if user in user_info:
			break
		else:
			print('Client not found')
	
	listening_thread = threading.Thread(target=listening, args=(user,))
	get_input_thread = threading.Thread(target=get_input, args=(user,))
	
	listening_thread.start()
	get_input_thread.start()
	
	listening_thread.join()
	get_input_thread.join()