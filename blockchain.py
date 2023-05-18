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
		self.previous_hash = previous_hash
		self.hash = self.calculate_hash()

	def calculate_hash(self):
		data_string = json.dumps(self.__dict__, sort_keys=True)
		return hashlib.sha256(data_string.encode()).hexdigest()


class Blockchain:
	def __init__(self):
		self.chain = [self.create_genesis_block()]

	def create_genesis_block(self):
		return Block(0, add_timestamp(), "Genesis Block", "0")

	def create_block(self, msg):
		index = len(self.chain)
		previous_hash = self.chain[-1].hash
		new_block = Block(index, add_timestamp(), msg, previous_hash)
		return new_block

	def add_block(self, msg):
		new_block = self.create_block(msg)
		self.chain.append(new_block)

	def get_block(self, hash):
		for block in self.chain:
			if block.hash == hash:
				return block
		return None

	def get_all_blocks(self):
		return self.chain
