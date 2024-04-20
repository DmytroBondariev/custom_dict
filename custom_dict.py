from typing import Any


class Dictionary:
    """
    A custom implementation of a dictionary (hashmap) in Python.

    This implementation uses separate chaining for collision resolution, which involves
    using an array of linked lists (or Python lists in this case) to handle collisions.
    When two keys hash to the same index, they are stored in the same bucket (list).

    The load factor is used to determine when to resize the dictionary. If the number of
    entries exceeds a certain proportion of the total capacity (2/3 in this case), the
    hashmap is resized. Resizing involves creating a new array of buckets with double the
    capacity and rehashing all the entries. This can be expensive, but it helps to maintain
    a balanced load factor and prevent long chains.

    The built-in Python `hash` function is used to compute the hash of the keys. This function
    is designed to provide a good distribution of hash values for a wide range of inputs.

    The dictionary also supports deletion of keys with the `__delitem__` method. If the load factor
    falls below a quarter after a deletion, the dictionary is resized to half its current capacity.

    The `_resize` method is used to resize the dictionary. If the 'smaller' flag is True, it halves
    the capacity of the dictionary. Otherwise, it doubles the capacity. It then rehashes all the
    key-value pairs.
    """

    def __define_potential_capacity_increase(self, previous_capacity: int = 8):
        """
        Defines the potential capacity increase of the dictionary based on the load factor and the current size.
        """

        while previous_capacity * self.load_factor < self.size:
            previous_capacity *= 2

        return int(previous_capacity)

    def __define_potential_capacity_decrease(self, previous_capacity: int = 8):
        """
        Defines the potential capacity decrease of the dictionary based on the load factor and the current size.
        """

        while previous_capacity / 2 * self.load_factor > self.size:
            previous_capacity /= 2

        return int(previous_capacity)

    def _capacity_recalculation(self, increased=False):
        """
        Defines the potential capacity decrease of the dictionary based on the load factor and the current size.
        """
        if self.size / self.capacity >= self.load_factor:
            self._resize(smaller=increased)

    @staticmethod
    def validate_keys(keys):
        """
        Validates the keys to ensure they are hashable.
        """
        return all(hasattr(key, "__hash__") for key in keys)

    def __init__(self, initial_capacity: int = 8, load_factor: float = 2 / 3, **kwargs) -> None:
        """
        Initializes the dictionary with a certain capacity and load factor.
        Also, it accepts keyword arguments to initialize the dictionary with key-value pairs.
        """
        if self.validate_keys(kwargs.keys()):
            self.load_factor = load_factor
            self.size = len(kwargs) if kwargs else 0
            self.capacity = self.__define_potential_capacity_increase(initial_capacity)
            self.buckets = [[] for _ in range(self.capacity)]

            for key, value in kwargs.items():
                bucket_index = self._get_bucket_index(key)
                bucket = self.buckets[bucket_index]

                for i, (stored_key, stored_value, stored_hash) in enumerate(bucket):
                    if stored_key == key:
                        bucket[i] = (key, value, hash(key))
                        return

                bucket.append((key, value, hash(key)))

        else:
            raise ValueError("Keys must be hashable")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Adds a key-value pair to the dictionary. If the load factor is exceeded, it resizes
        the dictionary. If the key already exists, it updates the value.
        """
        self.size += 1
        self._capacity_recalculation()

        bucket_index = self._get_bucket_index(key)
        bucket = self.buckets[bucket_index]

        for i, (stored_key, stored_value, stored_hash) in enumerate(bucket):
            if stored_key == key:
                bucket[i] = (key, value, hash(key))
                return

        bucket.append((key, value, hash(key)))

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieves the value associated with a given key. If the key does not exist, it raises a KeyError.
        """
        bucket_index = self._get_bucket_index(key)
        bucket = self.buckets[bucket_index]

        for stored_key, stored_value, stored_hash in bucket:
            if stored_key == key:
                return stored_value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        """
        Removes a key-value pair from the dictionary. If the load factor falls below a quarter, it resizes
        the dictionary to half its current capacity. If the key does not exist, it raises a KeyError.
        """
        bucket_index = self._get_bucket_index(key)
        bucket = self.buckets[bucket_index]

        for i, (stored_key, _, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[i]
                self.size -= 1
                if self.size < self.capacity // 4:
                    self._resize(smaller=True)
                return

        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Checks if a key is in the dictionary.
        """
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __iter__(self):
        """
        Yields each key-value pair in the dictionary.
        """
        for bucket in self.buckets:
            for key, value, _ in bucket:
                yield key, value

    def __len__(self) -> int:
        """
        Returns the number of key-value pairs in the dictionary.
        """
        return self.size

    def _get_bucket_index(self, key: Any) -> int:
        """
        Returns the index of the bucket where a key should be stored. If the key already exists,
        it returns the index of the bucket where the key is stored.
        """
        hash_value = hash(key)
        initial_index = hash_value % self.capacity
        bucket_index = initial_index

        bucket = self.buckets[bucket_index]

        while bucket:
            for stored_key, _, _ in bucket:
                if stored_key == key and type(stored_key) is type(key):
                    return bucket_index
            bucket_index = (bucket_index + 1) % self.capacity
            bucket = self.buckets[bucket_index]

            if bucket_index == initial_index:
                raise KeyError(key)

        return bucket_index

    def _resize(self, smaller=False) -> None:
        """
        Resizes the dictionary. If the 'smaller' flag is True, it halves the capacity of the dictionary.
        Otherwise, it doubles the capacity. It then rehashes all the key-value pairs.
        """
        new_capacity = self.__define_potential_capacity_decrease(self.capacity) if smaller \
            else self.__define_potential_capacity_increase(self.capacity)

        new_buckets = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for key, value, _ in bucket:
                bucket_index = hash(key) % new_capacity
                new_buckets[bucket_index].append((key, value, hash(key)))

        self.buckets = new_buckets
        self.capacity = new_capacity
