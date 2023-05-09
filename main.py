import hashlib
import json
import socket

import blockchain as bc
import p2p_communicate as p2p

blockchain = bc.Blockchain()

opponentIP = "localhost"
opponentPORT = 12345
def communicate():
	with p2p.p2pconnect_to(opponentIP, opponentPORT) as opponent:
		while True:
			thread1 = threading.Thread(target = receive, args = ([s]))
			thread2 = threading.Thread(target = send, args = ([s]))
			thread1.start()
			thread2.start()
			thread1.join()
			thread2.join()
			

	
async def send(s):
	message = input('Enter a message: ')
	if message == 'display chain':
		print(blockchain.get_all_blocks())
	else:
		opponent.send(message.encode())
		data = opponent.recv(1024)
		response = data.decode()
		blockchain.add_block(message)
		print('Server response:', response)

		last_block_hash = blockchain.chain[-1].hash
		block = blockchain.get_block(last_block_hash)
		if block is not None:
			print("Found block with hash {}: {}".format(last_block_hash, block.__dict__))
		else:
			print("No block found with hash {}".format(last_block_hash))
	

HOST = ''
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

async def receive(s):
	client_socket, client_address = server_socket.accept()
	print(f'Connection from {client_address}')

	data = client_socket.recv(1024)
	print(f'Received: {data.decode()}')

	response = 'Hello, client!'.encode()
	client_socket.sendall(response)

	client_socket.close()
	


	

