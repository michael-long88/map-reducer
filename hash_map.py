from linked_list import LinkedList


class HashMap:
    def __init__(self):
        self.TABLE_SIZE = 53
        self.table = [None] * self.TABLE_SIZE

    def hash_string(self, unhashed_string: str):
        total_ascii_sum = sum([ord(c) for c in unhashed_string])
        return total_ascii_sum % self.TABLE_SIZE

    def add_to_hash_table(self, hashed_index: int, unhashed_value):
        if self.table[hashed_index] is None:
            self.table[hashed_index] = unhashed_value
        elif isinstance(self.table[hashed_index], LinkedList):
            self.table[hashed_index].insert(unhashed_value)
        else:
            bucket = LinkedList()
            bucket.insert(self.table[hashed_index])
            bucket.insert(unhashed_value)
            self.table[hashed_index] = bucket
