import hashlib

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
			'file': None,
			'data_key': hash_to_num(1000, 10000, data),
			'sender': None
		}
		dataset.update(data)
		return dataset
		
	def insert(self, **kwargs):
		key = self.key(kwargs)
		self.database[key] = self.create_data(kwargs)

	def get(self, **kwargs):
		key = self.key(kwargs)
		with open('data.json', 'w') as db:
			db.write(str(self.database))
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
		'data': "b'gh9tw43htt"
	}
	db.insert(sender = 'sender', text = 'text', file = file)
	print(db.get(sender = 'sender', text = 'text', file = file))