import hashlib
import json
import datetime

def add_timestamp():
	now = datetime.datetime.now()
	formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
	return formatted_date


class Block:
	def __init__(self, index, timestamp, msg, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.msg = msg
		self.file_data = None
		self.previous_hash = previous_hash
		self.hashed_number = 0
		self.hash = self.calculate_hash()

	def calculate_hash(self):
		data_string = json.dumps(self.__dict__, sort_keys=True)
		return hashlib.sha256(data_string.encode()).hexdigest()


class Blockchain:
	def __init__(self):
		self.chain = [self.create_genesis_block()]
		self.range_min = 0
		self.range_max = 10000
		
	def hash_to_number(self, *args):
		number = 0
		for arg in args:
			hashed_value = hash(arg)
			number = number + (hashed_value % (self.range_max - self.range_min + 1)) + self.range_min
		return number

	def create_genesis_block(self):
		return Block(0, add_timestamp(), "Genesis Block", "0")

	def create_block(self, msg=None, file=None):
		index = len(self.chain)
		previous_hash = self.chain[-1].hash
		new_block = Block(index, add_timestamp(), msg, hash_to_number(msg, file), previous_hash)
		return new_block

	def add_block(self, msg=None, file=None):
		new_block = self.create_block(msg)
		self.chain.append(new_block)

	def get_block(self, hash):
		for block in self.chain:
			if block.hash == hash:
				return block
		return None

	def get_all_blocks(self):
		return self.chain
