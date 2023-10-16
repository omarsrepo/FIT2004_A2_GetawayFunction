from assignment2 import load_dictionary


class Node:
    def __init__(self, label=None):
        self.label = label
        self.size = 27
        self.link = [None] * self.size

        self.terminal = False
        self.definition = None
        self.frequency = None

    def __repr__(self):
        return f"Node({self.label})"


class Trie:
    def __init__(self, Dictionary: list[list]):
        self.root = Node()
        for item in Dictionary:
            word, definition, frequency = item[0], item[1], item[2]
            self.insert(word, definition, frequency)

    def insert(self, word, definition, frequency):
        # Begin from root
        current = self.root

        for char in word:
            # If path exists
            index = ord(char) - 96
            if current.link[index] is not None:
                current = current.link[index]
            else:
                current.link[index] = Node(char)
                current = current.link[index]

        current.terminal = True
        current.definition = definition
        current.frequency = frequency

    def prefix_search(self, prefix: str):
        count = 0
        max_frequency = 0
        current = self.root

        # Moving the pointer to the end of the prefix to begin search
        for char in prefix:
            index = ord(char) - 96
            if current.link[index]:
                current = current.link[index]
            else:
                # If the prefix does not exist in the TRIE
                return [None, None, 0]

        # Initialize result and count
        result = [None, None, 0, 0]  # [word, definition, count]
        count = 0

        # Perform DFS traversal
        self.dfs_traversal(current, prefix, result, count)
        result.remove(result[2])
        return result

    def dfs_traversal(self, node, prefix, result, count):
        if node.terminal:
            result[3] += 1
            if node.frequency > result[2]:
                result[0] = prefix
                result[1] = node.definition
                result[2] = node.frequency

        for i, child in enumerate(node.link):
            if child is not None:
                self.dfs_traversal(child, prefix + child.label, result, count)

# current = my_trie.root
# for char in 'abaca':
#     print(current.link[ord(char)-96])
#     print(current.link[ord(char) - 96].link)
#     print(current.link[ord(char) - 96].terminal)
#     print()
#     current = current.link[ord(char)-96]


if __name__ == "__main__":
    Dictionary = load_dictionary("Dictionary.txt")
    my_trie = Trie(Dictionary)
    print(my_trie.prefix_search('a'))

