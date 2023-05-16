import tkinter as tk
import threading
import socket

import blockchain
import p2p_communicate as p2p

client_info = {'Keyhole': ('localhost', 42345), 'Kamina': ('localhost', 49000), 'Kjavik': ('localhost', 48000)}

bc = blockchain.Blockchain()

def send_data(opponent_name, data, sender_name):
	try:
		if opponent_name in client_info:
			op_ip, op_port = client_info[opponent_name]
			with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
				if 'png' in data:
					with open(data, 'rb') as file:
						file_data = file.read()
						op_socket.sendall(file_data)
				op_socket.sendall(data.encode())
		else:
			print(f"Opponent '{opponent_name}' does not exist in client_info.")
	except KeyError:
		print(f"Opponent '{opponent_name}' does not exist in client_info.")
	except Exception as e:
		print('Error:', e)

	
def listening(client_name):
	ip_address, port = client_info[client_name]
	receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	receive_socket.bind((ip_address, port))
	receive_socket.listen()
	while True:
		try:
			client_socket, client_address = receive_socket.accept()
			for name, address in client_info.items():
				if address == client_address:
					client_name = name
					break
			data = client_socket.recv(1024).decode()
			print(client_name, ':', data)
		except Exception:
				pass

def get_input(user):
	global client_info
	def handle_return(event):
		msg = entry.get()
		if ':' in msg:
			message = msg.split(":")
			opponent_name = message[0]
			data = message[1]
			if opponent_name in client_info:
				send_data(opponent_name, data, user)
			elif opponent_name == 'all':
				for client in client_info.keys():
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
		if user in client_info:
			break
		else:
			print('Client not found')
	
	listening_thread = threading.Thread(target=listening, args=(user,))
	get_input_thread = threading.Thread(target=get_input, args=(user,))
	
	listening_thread.start()
	get_input_thread.start()
	
	listening_thread.join()
	get_input_thread.join()