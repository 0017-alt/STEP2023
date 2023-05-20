import random, sys, time, gc

# Assigning primes to each alphabets
# The matchings are as follows:
#                      a   b   c   d   e   f   g   h   i   j   k   l   m   n   o   p   q   r   s   t    u    v    w    x    y    z
#			          -------------------------------------------------------------------------------------------------------------
prime_list_alphabet = [5,  7,  11, 13, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 79, 83, 89, 97, 101, 103, 109, 113, 127, 131]

#                     0    1    2    3    4    5    6    7    8    9
#                   ---------------------------------------------------
prime_list_number = [137, 139, 149, 157, 163, 167, 173, 179, 181, 191]


# Define the list of a buket size
# Have several candidates for re-hashing
bucket_size_list = [17 ,37, 73, 151, 353, 701, 1453, 2861, 5449, 10663, 31607, 62053, 104729]

# Hash function.
#
# |key|: string
# Return value: a hash value
# Create a hash value by multiplying by the corresponding prime number
def calculate_hash(key):
	assert type(key) == str
	hash = 0
	for i in key:
		if (97 <= ord(i) and ord(i) <= 122):
			hash += prime_list_alphabet[ord(i) - 97]
		elif (48 <= ord(i) and ord(i) <= 57):
			hash += prime_list_number[ord(i) - 48]
	return hash

# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_index| : The index of the current index in the backet_size_list.
# |self.bucket_size|: The bucket size.
# |self.buckets|    : An array of the buckets. self.buckets[hash % self.bucket_size]
#                     stores a linked list of items whose hash value is |hash|.
# |self.item_count| : The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
	def __init__(self):
        # Set the initial bucket size. A prime number is chosen to reduce
        # hash conflicts.
		self.bucket_index = 0
		self.bucket_size = bucket_size_list[self.bucket_index]
		self.buckets = [None] * self.bucket_size
		self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|       : The key of the item.
    # |value|     : The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
	def put(self, key, value):
		assert type(key) == str
		self.check_size()
		# If occupancy exceeds 70%, expand the bucket size
		if (HashTable.size_notification(self) == 2):
			self = HashTable.rehash_expand(self)
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				item.value = value
				return False
			item = item.next
		new_item = Item(key, value, self.buckets[bucket_index])
		self.buckets[bucket_index] = new_item
		self.item_count += 1
		return True

    # Get an item from the hash table.
    #
    # |key|       : The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
	def get(self, key):
		assert type(key) == str
		self.check_size()
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				return (item.value, True)
			item = item.next
		return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
	def delete(self, key):
		assert type(key) == str
		self.check_size()
		# If occupancy falls below 30%, reduce the bucket size
		if (HashTable.size_notification(self) == 1):
			self = HashTable.rehash_reduce(self)
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if not item.next:
				if item.key == key:
					self.buckets[bucket_index] = None
					# Delete the item and release the memory
					del item
					gc.collect()
					self.item_count -= 1
					return True
			else:
				if item.key == key:
					self.buckets[bucket_index] = item.next
					del item
					gc.collect()
					self.item_count -= 1
					return True
				elif item.next.key == key:
					# Reconnect with the grandchild
					tmp = item.next
					item.next = item.next.next
					# Delete the item and release the memory
					del tmp
					gc.collect()
					self.item_count -= 1
					return True
			item = item.next
		return False

  # Return the total number of items in the hash table.
	def size(self):
		return self.item_count

	# Check that the hash table has a "reasonable" bucket size.
	# The bucket size is judged "reasonable" if it is smaller than 100 or
	# the buckets are 30% or more used.
	#
	# Note: Don't change this function.
	def check_size(self):
		assert (self.bucket_size < 100 or
				self.item_count >= self.bucket_size * 0.3)
	# Return 2 when occupancy exceeds 70%
	# Return 1 when occupancy falls below 30%
	# Otherwise, return 0
	def size_notification(self):
		if (self.item_count > self.bucket_size * 0.7):
			return 2
		elif (self.item_count < self.bucket_size * 0.3):
			return 1
		else:
			return 0

	# Expand the bucket if the occupancy exceeds 70%
	def rehash_expand(self):
		new_hash_table = HashTable()
		new_hash_table.bucket_index = self.bucket_index + 1
		if (new_hash_table.bucket_index >= len(bucket_size_list)):
			print("Upper Limit of the bucket size")
			return self
		new_hash_table.bucket_size = bucket_size_list[new_hash_table.bucket_index]
		new_hash_table.buckets = [None] * new_hash_table.bucket_size
		# Replacing elements in the old hashtable to the new hashtable
		for i in range(self.bucket_size):
			item = self.buckets[i]
			while item:
				new_hash_table.put(item.key, item.value)
				item = item.next
		return new_hash_table

	# Reducing the bucket if the occupancy falls below 30%
	def rehash_reduce(self):
		new_hash_table = HashTable()
		new_hash_table.bucket_index = self.bucket_index - 1
		if (new_hash_table.bucket_index < 0):
			return self
		new_hash_table.bucket_size = bucket_size_list[new_hash_table.bucket_index]
		new_hash_table.buckets = [None] * new_hash_table.bucket_size
		# Replacing elements in the old hashtable to the new hashtable
		for i in range(self.bucket_size):
			item = self.buckets[i]
			while item:
				new_hash_table.put(self.item.key, self.item.value)
				item = item.next
		return new_hash_table


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
