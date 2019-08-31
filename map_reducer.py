from linked_list import LinkedList, Node
from hash_map import HashMap
from operator import itemgetter
import operator


class Mapper:
    def __init__(self, text_location: str):
        self.punctuation = ['.', ',' '?', '!', ';', ':', '-', '[', ']', '{', '}', '(', ')', '"', "'", '\n', '–', '']
        self.text_location = text_location
        self.hash_maps = []
        self.line_count = 0

    def read_text(self):
        with open(self.text_location, 'r', encoding='utf-8') as text:
            hash_map = HashMap()
            for line in text:
                if line == '\n':
                    continue
                hash_map = self.add_words_to_hash_map(hash_map, line.lower())
                self.line_count += 1
            self.hash_maps.append(hash_map)

    def add_words_to_hash_map(self, current_hash_map: HashMap, current_line: str):
        if self.line_count >= 50:
            self.line_count = 0
            self.hash_maps.append(current_hash_map)
            current_hash_map = HashMap()
        split_line = current_line.split(' ')
        if '\n' in split_line:
            split_line.remove('\n')
        if '' in split_line:
            split_line.remove('')
        for word in self.strip_punctuation(split_line):
            if word in self.punctuation:
                continue
            map_index = current_hash_map.hash_string(word)
            current_hash_map.add_to_hash_table(map_index, (word, 1))
        return current_hash_map

    def strip_punctuation(self, words: list):
        for word in words:
            word_lst = list(word)
            if word_lst[0] in self.punctuation:
                word_lst[0] = ''
            if word_lst[-1] in self.punctuation:
                word_lst[-1] = ''
            word = ''.join(word_lst)
            yield word


class Reducer:
    def __init__(self, hash_maps: list):
        self.hash_maps = hash_maps
        self.reduced_hash_map = HashMap()
        self.top_ten_words = []

    def reduce(self):
        for hash_map in self.hash_maps:
            for bucket in hash_map.table:
                self.add_to_new_hash_table(bucket)

    def add_to_new_hash_table(self, bucket):
        if isinstance(bucket, LinkedList):
            self.add_linked_list_to_new_hash_table(bucket)
        elif isinstance(bucket, tuple):
            hashed_key = self.reduced_hash_map.hash_string(bucket[0])
            self.reduced_hash_map.add_to_hash_table(hashed_key, (bucket[0], 1))

    def add_linked_list_to_new_hash_table(self, bucket: LinkedList):
        bucket_keys = []
        for node in bucket.traverse():
            if node.data[0] in bucket_keys:
                continue
            if isinstance(node.data, tuple):
                bucket_keys = self.add_nodes_to_new_hash_table(bucket_keys, bucket, node)

    def add_nodes_to_new_hash_table(self, bucket_keys: list, current_bucket: LinkedList, current_node: Node) -> list:
        current_count = 0
        bucket_keys.append(current_node.data[0])
        for next_node in current_bucket.traverse():
            if next_node.data[0] == current_node.data[0]:
                current_count += 1
        hashed_key = self.reduced_hash_map.hash_string(current_node.data[0])
        self.reduced_hash_map.add_to_hash_table(hashed_key, (current_node.data[0], current_count))
        return bucket_keys

    def get_top_ten_words(self):
        top_words_per_bucket = []
        for bucket in self.reduced_hash_map.table:
            if isinstance(bucket, tuple):
                top_words_per_bucket.append(bucket)
            elif isinstance(bucket, LinkedList):
                top_three = [(" ", 0), (" ", 0), (" ", 0)]
                for node in bucket.traverse():
                    top_three.sort(key=itemgetter(1))
                    for index, value in enumerate(top_three):
                        if node.data[1] > value[1]:
                            top_three[index] = node.data
                            break
                top_words_per_bucket.extend(top_three)
        top_words_per_bucket.sort(key=itemgetter(1))
        return top_words_per_bucket[-10:]


class MapReducer:
    def __init__(self, text_location):
        self.text_location = text_location
        self.punctuation = ['.', ',' '?', '!', ';', ':', '-', '[', ']', '{', '}', '(', ')', '"', "'", '\n', '–', '']
        self.word_count_lst = []
        self.word_counts = {}
        self.line_count = 0
        self.reduced_word_counts = {}

    def read_text(self):
        with open(self.text_location, 'r', encoding='utf-8') as text:
            for line in text:
                if line == '\n':
                    continue
                self.add_words(line.lower())
                self.line_count += 1
            self.word_count_lst.append(self.word_counts)

    def add_words(self, current_line: str):
        if self.line_count >= 50:
            self.line_count = 0
            self.word_count_lst.append(self.word_counts)
            self.word_counts = {}
        split_line = current_line.split(' ')
        if '\n' in split_line:
            split_line.remove('\n')
        if '' in split_line:
            split_line.remove('')
        for word in self.strip_punctuation(split_line):
            if word in self.punctuation:
                continue
            if word not in self.word_counts.keys():
                self.word_counts[word] = 1
            else:
                self.word_counts[word] += 1

    def strip_punctuation(self, words):
        for word in words:
            word_lst = list(word)
            if word_lst[0] in self.punctuation:
                word_lst[0] = ''
            if word_lst[-1] in self.punctuation:
                word_lst[-1] = ''
            word = ''.join(word_lst)
            yield word

    def reduce(self):
        for word_count in self.word_count_lst:
            for key, value in word_count.items():
                if key in self.reduced_word_counts.keys():
                    self.reduced_word_counts[key] += value
                else:
                    self.reduced_word_counts[key] = value

    def get_top_ten_words(self):
        return sorted(self.reduced_word_counts.items(), key=operator.itemgetter(1))[-10:]
