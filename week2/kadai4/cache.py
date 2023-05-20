import sys, gc, random

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.

# Assigning primes to each alphabets
# The matchings are as follows:
#                      a   b   c   d   e   f   g   h   i   j   k   l   m   n   o   p   q   r   s   t    u    v    w    x    y    z
#			          -------------------------------------------------------------------------------------------------------------
prime_list_alphabet = [5,  7,  11, 13, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 79, 83, 89, 97, 101, 103, 109, 113, 127, 131]

#                     0    1    2    3    4    5    6    7    8    9
#                   ---------------------------------------------------
prime_list_number = [137, 139, 149, 157, 163, 167, 173, 179, 181, 191]

# Hash function.
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
class Item_hash:
    # |key|         : The ley of the item. The key must be a string.
    # |value|       : The index in chache
    # |next|        : The next item in the linked list. If this is the last item in the
    #                 linked list, |next| is None.
    # |next_cache|  : The item that acceced next
    # |before_cache|: The item that accesed before
    def __init__(self, url, contents, next):
        assert type(url) == str
        self.key = url
        self.value = contents
        self.next = next
        self.next_cache = None
        self.before_cache = None

# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|    : An array of the buckets. self.buckets[hash % self.bucket_size]
#                     stores a linked list of items whose hash value is |hash|.
# |self.item_count| : The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
	def __init__(self):
        # Set the initial bucket size to 17. A prime number is chosen to reduce
        # hash conflicts.
		self.bucket_size = 17
		self.buckets = [None] * self.bucket_size
		self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|       : The key of the item.
    # |value|     : The value of the item.
    # Return value: The corresponding item
	def put(self, key, value):
		assert type(key) == str
		self.check_size()
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				item.value = value
				return item
			item = item.next
		new_item = Item_hash(key, value, self.buckets[bucket_index])
		self.buckets[bucket_index] = new_item
		self.item_count += 1
		return new_item

    # Get an item from the hash table.
    #
    # |key|       : The key.
    # Return value: If the item is found, (the item, True) is
    #               returned. Otherwise, (None, False) is returned.
	def get(self, key):
		assert type(key) == str
		self.check_size()
		bucket_index = calculate_hash(key) % self.bucket_size
		item = self.buckets[bucket_index]
		while item:
			if item.key == key:
				return (item, True)
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

class Cache:
    # Initialize the cache.
    # |n|        : The size of the cache.
    # |oldest|   : The item of the chache that holds oldest chache
    # |newest|   : The item of the chache that holds newest chache
    # |hashtable|: The hashtable
    def __init__(self, n):
        assert type(n) == int
        self.n = n
        self.oldest = None
        self.newest = None
        self.hashtable = HashTable()

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        response = HashTable.get(self.hashtable, url)
        if (response[1]):
            if (response[0] == self.newest):
                return
            elif (response[0] == self.oldest):
                tmp = self.oldest
                self.oldest = tmp.next_cache
                self.newest = tmp
            elif (response[0] == self.oldest.next_cache):
                self.oldest.next_cache = response[0].next_cache
                response[0].next_cache.before_cache = self.oldest
                self.newest.next_cache = response[0]
                response[0].before_cache = self.newest
                response[0].next_cache = self.oldest
                self.oldest.before_cache = response[0]
                self.newest = response[0]
            elif (response[0] == self.newest.before_cache):
                self.newest.before_cache = response[0].before_cache
                response[0].before_cache.next_cache = self.newest
                self.newest.next_cache = response[0]
                response[0].before_cache = self.newest
                response[0].next_cache = self.oldest
                self.oldest.before_cache = response[0]
                self.newest = response[0]
        else:
            item_count = self.hashtable.item_count
            if (item_count == 0):
                new_item = HashTable.put(self.hashtable, url, contents)
                new_item.before_cache = new_item
                new_item.next_cache = new_item
                self.newest = new_item
                self.oldest = new_item
            elif (item_count < self.n):
                new_item = HashTable.put(self.hashtable, url, contents)
                self.newest.next_cache = new_item
                new_item.before_cache = self.newest
                self.oldest.before_cache = new_item
                new_item.next_cache = self.oldest
                self.newest = new_item
            else:
                new_item = HashTable.put(self.hashtable, url, contents)
                tmp = self.oldest
                self.oldest = self.oldest.next_cache
                self.newest.next_cache = new_item
                new_item.before_cache = self.newest
                self.oldest.before_cache = new_item
                new_item.next_cache = self.oldest
                self.newest = new_item
                HashTable.delete(self.hashtable, tmp.key)

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        li = []
        if self.hashtable.item_count == 0:
            return li

        node = self.newest
        li.append(node.key)
        node = node.before_cache
        while not (node == self.newest):
            li.append(node.key)
            node = node.before_cache
        return li


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
