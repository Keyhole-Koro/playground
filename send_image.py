import socket

def send_image(image_path, host, port):
	receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		receiver_socket.connect((host, port))

		with open(image_path, 'rb') as file:
			image_data = file.read()
		receiver_socket.sendall(image_data)

		print("Image sent successfully.")
	except Exception as e:
		print("Error sending image:", e)
	finally:
		receiver_socket.close()

if __name__ == '__main__':
	image_path = "C:/Users/kiho/OneDrive/ドキュメント/Liquia - Copy/materials/github-icon.png"

	host = 'localhost'
	port = 42345

	send_image(image_path, host, port)
