import tkinter as tk
import threading
import socket
from pathlib import Path
import os
import json
import base64
from datetime import datetime

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

import base64

def send_file(opponent_name=None, text=None, file={}, sender=None):
    try:
        if opponent_name in client_info:
            op_ip, op_port = client_info[opponent_name]
            with p2p.p2pconnect_to(op_ip, op_port) as op_socket:
                file_name = file['file_name']
                file_extension = file['file_extension']
                file_b_data = file['file_b_data']
                file_data_encoded = base64.b64encode(file_b_data).decode('utf-8')

                all_data = {
                    'sender': sender,
                    'text': text,
                    'file': {
                        'file_name': file_name,
                        'file_extension': file_extension,
                        'file_b_data': file_data_encoded
                    }
                }

                data_json = json.dumps(all_data)
                data_bytes = data_json.encode('utf-8')
                op_socket.sendall(data_bytes)
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
			data = json.loads(client_socket.recv(100000).decode())
			sender = data['sender']
			if data['text']:
				text = data['text']
			if data['file']:
				file = data['file']
				file_name = file['file_name']
				file_extension = file['file_extension']
				file_b_data = file['file_b_data']
				
				current_time = datetime.now()
				formatted_time = str(current_time.strftime("%Y-%m-%d %H:%M:%S"))
				
				with open(f"C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/{file_name}.{file_extension}", 'wb') as f:
					f.write(base64.b64decode(file_b_data))
			
		except Exception:
				pass

def get_input(sender):
	global client_info
	def handle_submit():
		opponent = entry.get()
		text = entry2.get()
		file_path = entry3.get()
		file_b_data = b''
		file_name = file_path.split('\\')[-1]
		file_extension = file_name.split('.')[-1]
		with open(file_path, 'rb') as fp:
			file_b_data = fp.read()
		
		data = {
				'file_name': file_name.split('.')[0],
				'file_extension': file_extension,
				'file_b_data': file_b_data
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

	submit_button = tk.Button(root, text="Send", command=handle_submit)
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