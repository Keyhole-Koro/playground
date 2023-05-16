import socket

def receive_video(host, port, save_path):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_socket.bind((host, port))

		server_socket.listen(1)
		print("Waiting for a connection...")
		file_data = b''
		i = 0
		client_socket, client_address = server_socket.accept()
		with open(save_path, "wb") as file:
			while True:
				
				print("Connected:", client_address)
				data = client_socket.recv(10010)
				print(i,'----------------------------------')
				if not data:
					print('no data')
					break
				file_data = file_data + data
				print(len(file_data))
				i = i + 1
			file.write(file_data)
			print("File received and saved successfully.")
	except Exception as e:
		print("Error:", e)
	finally:
		client_socket.close()
		server_socket.close()


if __name__ == '__main__':
	receive_video("localhost", 42345, "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/received_video2.mp4")
