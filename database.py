import hashlib

class Database:
	def __init__(self):
		self.database = {}
		
	def key(self, *args):
		range_min=1
		range_max=10
		number = 0
		for arg in args:
			if arg == None:
				continue
			hashed_value = hash(arg)
			print(hashed_value)
		return number + (hashed_value % (range_max - range_min + 1)) + range_min
		#return hashlib.sha256(msg.encode()).hexdigest()
	
	def data(self, )
	def insert(self, *args):
		hashed_key = hash_to_num(*args)
		key = self.key(*args)
		self.database[key] = args

	def get(self, *args):
		key = self.key(*args)
		return self.database.get(key)
	
range_min=1000
range_max=10000
def hash_to_num(*args):
	number = 0
	for arg in args:
		if arg == None:
			continue
		hashed_value = hash(arg)
		print(hashed_value)
	return number + (hashed_value % (range_max - range_min + 1)) + range_min
# Example usage
db = Database()
db.insert("apple", "apple")
db.insert("banana", "banana")

# Get values by hashed key
value1 = db.get("apple", "apple")
value2 = db.get("banana")

print(value1)
print(value2)

