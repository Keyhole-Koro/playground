import tkinter as tk
import threading
import socket
from pathlib import Path
import os

import blockchain
import p2p_communicate as p2p

client_info = {
	'user1': ('localhost', 42345),
	'user2': ('localhost', 49000),
	'user3': ('localhost', 48000),
	'user4': ('localhost', 43345),
	'user5': ('localhost', 44345),
	'user6': ('localhost', 45345),
	'user7': ('localhost', 46345),
	'user8': ('localhost', 47345),
	'user9': ('localhost', 48345),
	'user10': ('localhost', 49345)
	}

bc = blockchain.Blockchain()

def send_file(opponent_name = None, text = None, data = {}, sender = None):
	try:
		if opponent_name in client_info:
			op_ip, op_port = client_info[opponent_name]
			with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
				if data.split('.')[-1]:
					file_extension = data.split('.')[-1]
					with open(data, 'rb') as file:
						print('data', data)
						print('type(data)', type(data))
						file_data = file.read()
						print('file.read()', file.read())
						print('file_data', file_data)
						file_name = data
						print('type(sender_name)', type(sender_name))
						print('type(file_name)', type(file_name))
						print('type(extension)', type(extension))
						print('type(file_data)', type(file_data))
						add_data = f'{sender_name}:{file_name}:{extension}:{str(file_data)}'
						data = {
						'text': 'Hello, server!',
						'file_name': file_name,
						'file_extension': file_extension,
						'file_data': file_data
						}
						op_socket.sendall(add_data.encode())
				add_data = f'{sender_name}:{extension}:{data}'
				op_socket.sendall(add_data.encode())
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
			print('listening')
			data = client_socket.recv(100000).decode()
			print('listening1')
			split_data = data.split(':',4)
			sender_name = split_data[0]
			file_name = split_data[2]
			extension = split_data[3]
			file_data = split_data[4]
			print('listening2')
			#file_data = "b'"+file_data+"'"
			print(sender_name)
			print(file_name)
			print(extension)
			print('file_data', file_data)
			if extension == '':
				print(sender_name, ':', data)
			elif extension == 'png':
				print('png')
				with open('received_image.png', "wb") as file:
					print('file.write(file_data)', file_data)
					file.write(file_data)
		except Exception:
				pass

def get_input(sender):
    global client_info

    def handle_submit():
        opponent = entry.get()
        text = entry2.get()
        file_path = entry3.get()
		file_data = b''
		file_name = file_path.split('\\')[-1]
		file_extension = file_name.split('.')[-1]
		with open(file_path, 'rb') as fp:
			file_data = fp.read()
		
        data = {
				'file_name': file_name,
				'file_extension': file_extension,
				'file_data': file_data
				}
		send_file(opponent, text, data, sender)
        
        entry.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)

    root = tk.Tk()

    label = tk.Label(root, text="Enter your messages:")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    entry2 = tk.Entry(root)
    entry2.pack()

    entry3 = tk.Entry(root)
    entry3.pack()

    submit_button = tk.Button(root, text="Submit", command=handle_submit)
    submit_button.pack()

    root.mainloop()


if __name__ == '__main__':
	while True:
		user = input('Enter your name:')
		if user in client_info.keys():
			break
		else:
			print('Client not found')
	
	listening_thread = threading.Thread(target=listening, args=(user,))
	get_input_thread = threading.Thread(target=get_input, args=(user,))
	
	listening_thread.start()
	get_input_thread.start()
	
	listening_thread.join()
	get_input_thread.join()