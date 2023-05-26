import hashlib
import json
import base64

import blockchain as bc

class Database:
	def __init__(self):
		self.database = {}
		
	def key(self, *args):
		range_min=1
		range_max=10
		number = 0
		return hash_to_num(range_min, range_max, args)
		#return hashlib.sha256(msg.encode()).hexdigest()
	def create_data(self, data):
		dataset = {
			'timestamp': bc.add_timestamp(),
			'text': None,
			'file': None,#change to file path
			'data_key': hash_to_num(1000, 10000, data),
			'sender': None
		}
		dataset.update(data)
		return dataset
		
	def insert(self, **kwargs):
		key = self.key(kwargs)
		if kwargs['file']:
			d_file_ex_b_data = kwargs
			nested_file = d_file_ex_b_data.get('file')
			nested_file.pop('file_b_data')
			self.write_to_json(key, d_file_ex_b_data)
		
	def get(self, **kwargs):
		key = self.key(kwargs)
		return self.database.get(key)
	
	def write_to_json(self, key, file_details):
		try:
			with open('C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/data.json') as file:
				data = json.load(file)
				data[key] = self.create_data(file_details)
		except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
			print(f"Error loading JSON: {e}")
			data = {}
		print('data', data)
#doesnt work
def saved_path(file):
	print('file')
	file_path = f'C:/Users/kiho/OneDrive/デスクトップ/blockchain-playground/files/{file["file_name"]}.{file["file_extension"]}'
	print('file_path', file_path)
	with open(file_path, 'wb') as new_file:
		new_file.write(base64.b64decode(file['file_b_data']))
	return file_path
def hash_to_num(range_min, range_max, *args):
	number = 0
	for arg in args:
		for arg2 in arg:
			for arg3 in arg2:
				if arg3 == None:
					continue
				hashed_value = hash(arg3)
				number = number + (hashed_value % (range_max - range_min + 1)) + range_min
	return number

if __name__ == '__main__':
	file = {
		'file_name': 'file_name',
		'file_extension': 'png',
		'file_b_data': b'file_data_encoded'
	}
	saved_path(file)
	"""
	db = Database()
	file = {
		'name': 'Keyhole',
		'data': "b'gh56h56h5"
	}
	db.insert(sender = 'sender', text = 'text', file = file)
	print(db.get(sender = 'sender', text = 'text', file = file))
	"""