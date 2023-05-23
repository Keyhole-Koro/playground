import hashlib
import json

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
		try:
			with open('data.json') as file:
				data = json.load(file)
				data[key] = self.create_data(kwargs)
		except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
			print(f"Error loading JSON: {e}")
			data = {}
		print('data', data)
		
	def get(self, **kwargs):
		key = self.key(kwargs)
		return self.database.get(key)

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
	db = Database()
	file = {
		'name': 'Keyhole',
		'data': "b'gh56h56h5"
	}
	db.insert(sender = 'sender', text = 'text', file = file)
	print(db.get(sender = 'sender', text = 'text', file = file))