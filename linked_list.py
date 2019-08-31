class Node:
    def __init__(self, data, next_node=None):
        self._data = data
        self._next_node = next_node

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, next_node):
        self._next_node = next_node

    def __repr__(self):
        return repr(self.data)


class LinkedList:
    def __init__(self, head: Node = None):
        self.head = head
        self.size = 0 if self.head is None else 1

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, new_head):
        self._head = new_head

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size

    def insert(self, data):
        self.head = Node(data, self.head)
        self.size += 1

    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                break
            else:
                current_node = current_node.next_node
        if current_node is None:
            raise ValueError("Data is not in list")
        return current_node

    def delete(self, data):
        current_node = self.head
        previous = None
        while current_node and current_node.data != data:
            previous = current_node
            current_node = current_node.next_node
        if current_node is None:
            raise ValueError("Data is not in list")
        if previous is None:
            self.head = current_node.next_node
        else:
            previous.next_node = current_node.next_node
            current_node.next_node = None
        if self.head is None:
            self.size = 0
        else:
            self.size -= 1

    def traverse(self):
        current_node = self.head
        while current_node:
            yield current_node
            current_node = current_node.next_node

    def __repr__(self):
        if self.size == 0:
            return "Empty LinkedList"
        else:
            current_node = self.head
            linked_list_string = f"{current_node} --> "
            while current_node:
                linked_list_string += f"{current_node.next_node} --> " if current_node.next_node is not None else \
                    f"{current_node.next_node}"
                current_node = current_node.next_node
            return linked_list_string
