import tkinter as tk
import threading
import socket
from pathlib import Path
import os
import json
import base64
from datetime import datetime

import blockchain
import database as db
import p2p_communicate as p2p

node = {
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
db = db.Database()

def send(opponent_name=None, text=None, file=[], sender=None):
	try:
		if opponent_name in node.keys():
			op_ip, op_port = node[opponent_name]
			with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
				if file:
					file_name = file['file_name']
					file_extension = file['file_extension']
					file_b_data = file['file_b_data']
					file_data_encoded = base64.b64encode(file_b_data).decode('utf-8')
					file = {
						'file_name': file_name,
						'file_extension': file_extension,
						'file_b_data': file_data_encoded
					}
				else:
					pass
				data = {
					'sender': sender,
					'text': text,
					'file': file
				}
				data_json = json.dumps(data)
				data_bytes = data_json.encode('utf-8')
				op_socket.sendall(data_bytes)
				bc.add_block(data_bytes)
		else:
			print(f"Opponent '{opponent_name}' does not exist in node.")
	except KeyError as e:
		print(f"KeyError: '{e}' does not exist.")
	except Exception as e:
		print('Error:', e)
	except ValueError as v:
		print('ValueError:', v)

def transmit_data(opponent_name=None, text=None, l_file=[], sender=None):
	try:
		if opponent_name in node.keys():
			op_ip, op_port = node[opponent_name]
			with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
				data = sort_file_base64str(opponent_name, text, file, sender)
				data_bytes = convert_strdict_bytes(data)
				op_socket.sendall(data_bytes)
				bc.add_block(data_bytes)
		else:
			print(f"Opponent '{opponent_name}' does not exist in node.")
	except KeyError as e:
		print(f"KeyError: '{e}' does not exist.")
	except Exception as e:
		print('Error:', e)
	except ValueError as v:
		print('ValueError:', v)

def listening(client_name):
	ip_address, port = node[client_name]
	receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	receive_socket.bind((ip_address, port))
	receive_socket.listen()
	while True:
		try:
			client_socket, client_address = receive_socket.accept()
			data = json.loads(client_socket.recv(1000000).decode())
			sender = data['sender']
			text = None
			file = None
			if data['text']:
				text = data['text']
				print(f'{sender}:{text}')
			if data['file']:
				file = data['file']
				file_name = file['file_name']
				file_extension = file['file_extension']
				file_b_data = file['file_b_data']
				file_path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/{file["file_name"]}.{file["file_extension"]}'
				with open(file_path, 'wb') as new_file:
					new_file.write(base64.b64decode(file['file_b_data']))
				file['file_path'] = file_path
			print('insert')
			db.insert(sender = sender, text = text, file = file)
			print('insert1')
			print(db.get(text, file))
		except Exception:
				pass


def convert_strdict_bytes(string:str):
	string_json = json.dumps(string)
	string_bytes = string_json.encode('utf-8')
	return string_bytes

#make more abstract(arg kwarg)
def sort_file_base64str(opponent_name, text, file:list, sender):->list
	file_name = file['file_name']
	file_extension = file['file_extension']
	file_b_data = file['file_b_data']
	file_data_encoded = base64.b64encode(file_b_data).decode('utf-8')
	sorted_file = {
		'file_name': file_name,
		'file_extension': file_extension,
		'file_b_data': file_data_encoded
	}
	sorted_data = {
		'sender': sender,
		'text': text,
		'file': sorted_file
	}
	return sorted_data

def pull_request():
	pass

def arrange_data(file_path, file_b_data):->dict
	file_name_ext = file_path.split('\\')[-1]
	file_name = file_name_ext.split('.')[0]
	file_extension = file_name_ext.split('.')[-1]

	file = {
		'file_name': file_name,
		'file_extension': file_extension,
		'file_b_data': file_b_data
	}
	return file

def file_part():
	pass

def split_file(file_path, file_b_data):->list
	chunks = divide_into_chunks(file_b_data, 90000)
	file = arrange_data(file_path, None)
	files = []
	for c in range(len(chunks)):
		chunk = chunks[c]
		file['part_num'] = c
		file['file_b_data'] = chunk
		files.append(file)
	return files

def divide_into_chunks(string, chunk_size):->list
	chunks = [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]
	return chunks

def handle_submit(entry, entry2, entry3, sender):
	opponent = entry.get().strip()
	text = entry2.get()
	file_path = entry3.get().strip().replace('"', '')

	if file_path:
		with open(file_path, 'rb') as fp:
			file_b_data = fp.read()
			print(len(file_b_data))
		if len(file_b_data) < 90000:
			l_file = split_file(file_path, file_b_data)
		else:
			#file = handle_huge_file(file_path, file_b_data)
			l_file = split_file(file_path, file_b_data)
	else:
		l_file = []
	send(opponent, text, l_file, sender)

	#entry.delete(0, tk.END)
	entry2.delete(0, tk.END)
	entry3.delete(0, tk.END)


def get_input(sender):
	root = tk.Tk()

	label = tk.Label(root, text="Enter your messages:")
	label.pack()

	entry = tk.Entry(root)
	entry.pack()

	entry2 = tk.Entry(root)
	entry2.pack()

	entry3 = tk.Entry(root)
	entry3.pack()

	submit_button = tk.Button(root, text="Send",
							  command=lambda: handle_submit(entry, entry2, entry3, sender))
	submit_button.pack()

	root.mainloop()

if __name__ == '__main__':
	while True:
		user = input('Enter your name:')
		if user in node.keys():
			break
		else:
			print('Client not found')
	
	listening_thread = threading.Thread(target=listening, args=(user,))
	get_input_thread = threading.Thread(target=get_input, args=(user,))
	
	listening_thread.start()
	get_input_thread.start()
	
	listening_thread.join()
	get_input_thread.join()