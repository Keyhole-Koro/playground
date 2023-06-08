import socket

def send_file(file_path, host, port):
	sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sender_socket.connect((host, port))

		with open(file_path, 'rb') as file:
			file_data = file.read()

		sender_socket.sendall(file_data)

		print("Image sent successfully.")
	except Exception as e:
		print("Error sending image:", e)
	finally:
		sender_socket.close()

if __name__ == '__main__':
	file_path = "C:/Users/kiho/OneDrive/デスクトップ/playground/Video Countdown 27 Digital   10 seconds.mp4"
	host = 'localhost'
	port = 42345

	send_file(file_path, host, port)
