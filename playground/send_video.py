import socket

def send_file(file_path, host, port):
	sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sender_socket.connect((host, port))

		with open(file_path, 'rb') as file:
			file_data = file.read()
			chunk_size = 100000
			split_count = len(file_data)/chunk_size
			chunks = divide_into_chunks(file_data, chunk_size)
			for i in range(int(split_count)+1):
				print(i)
				sender_socket.sendall(chunks[i])
		print(len(file_data))
		print("Image sent successfully.")
	except Exception as e:
		print("Error sending image:", e)
	finally:
		sender_socket.close()
def divide_into_chunks(string, chunk_size):
	chunks = [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]
	return chunks
if __name__ == '__main__':
	file_path = "C:/Users/kiho/OneDrive/デスクトップ/playground/IDOL  Eurobeat Remix.mp4"
	host = 'localhost'
	port = 42345

	send_file(file_path, host, port)