import socket

def receive_image(host, port, save_path):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_socket.bind((host, port))

		server_socket.listen(1)
		print("Waiting for a connection...")

		with open(save_path, "wb") as file:
			while True:
				client_socket, client_address = server_socket.accept()
				print("Connected:", client_address)
				data = client_socket.recv(10000)
				print(data)
				if not data:
					print('no data')
					break
				file.write(data)
				print("File received and saved successfully.")
	except Exception as e:
		print("Error:", e)
	finally:
		client_socket.close()
		server_socket.close()


if __name__ == '__main__':
	receive_image("localhost", 42345, "C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/received_video.mp4")
