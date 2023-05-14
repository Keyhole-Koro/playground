import tkinter as tk
import threading
import socket
from blockchain import Blockchain

class Client:
	def __init__(self, name, ip_address, port):
		self.name = name
		self.ip_address = ip_address
		self.port = port

class P2PCommunication:
	def __init__(self, client_list):
		self.client_list = client_list
		self.client_socket = None
		self.bc = Blockchain()

	def send_message(self, message):
		if self.client_socket is None:
			try:
				self.first_contact(message)
			except Exception as e:
				print('Error connecting to opponent:', e)
		else:
			try:
				response = message.encode()
				self.client_socket.sendall(response)
				self.bc.add_block(message)
				print('You:', message)
			except Exception as e:
				print('Error sending message:', e)

	def first_contact(self, client_name):
		if client_name in self.client_list:
			ip_address, port = self.client_list[client_name]
			try:
				self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.client_socket.connect((ip_address, port))
				print('Successful connection')
				data = 'Successful connection'
				self.client_socket.sendall(data.encode())
			except Exception as e:
				print('Error connecting to client:', e)
		else:
			print('Client not found.')

	def first_listen(self, y_ip_address, y_port):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((y_ip_address, y_port))
		server_socket.listen()
		self.client_socket, client_address = server_socket.accept()
		print(f'Connection from {client_address}')

	def listen(self):
		while True:
			try:
				data = self.client_socket.recv(1024).decode()
				print('Opponent:', data)
			except Exception:
				pass

	def start(self):
		your_name = input('Tell me your name in advance: ')
		if your_name in self.client_list:
			y_ip_address, y_port = self.client_list[your_name]
		else:
			print('Invalid name')
			return
		thread1 = threading.Thread(target=self.send_message)
		thread2 = threading.Thread(target=self.first_listen, args=(y_ip_address, y_port))
		listening_thread = threading.Thread(target=self.listen)
		thread1.start()
		thread2.start()
		listening_thread.start()
		thread1.join()
		thread2.join()
		listening_thread.join()

	def get_blockchain(self):
		print(self.bc.get_all_blocks())


if __name__ == '__main__':
    client_info = {'Keyhole': ('localhost', 12345), 'Kamina': ('localhost', 19000)}
    p2p = P2PCommunication(client_info)
    p2p.start()

