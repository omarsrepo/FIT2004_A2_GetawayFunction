from assignment2 import load_dictionary


class Node:
    """
    Time complexity = O(1) for all operations
    Space complexity = Space for label O(n) + Space for size O(1) + Space for link O(27) + Space for terminal O(1) + Space for definition O(m) + Space for frequency O(1)
    Space complexity = O(n) + O(m) where n is the length of the word and m is the length of the definition
    """
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
        """
        Function description:
        Construction of the TRIE structure.

        :Input:
            argv1: Dictionary.txt file containing words with their descriptions and an assigned frequency.

        :Output, return or postcondition: TRIE data structure

        :Time complexity: Worst case time complexity of O(N*M) where N is the no.of words in the Dictionary and M is
                          the length of each word
        :Aux space complexity: O(n+m) * O(N) where (n+m) is the length of each word + length of word definition and N
                               is the total no.of words in the Dictionary. This adds up to the total no.of characters
                               in the dictionary which is O(T) overall worst case.
        """
        self.root = Node()
        for item in Dictionary:
            word, definition, frequency = item[0], item[1], item[2]
            self.insert(word, definition, frequency)

    def insert(self, word, definition, frequency):
        """
        Function description:
        Takes a word (eg: Jack) and inserts the word into the TRIE structure by traversing down the nodes one character
        at a time. If a node does not exist for that character, create a new node and continue.
        At the end of traversal of the word, place terminal and store relevant data (definition and frequency) into the
        terminal character's node.

        :Input:
            argv1: word
            argv2: definition of the word
            argv3: frequency assigned to the word

        :Output, return or postcondition: TRIE structure will contain the word.

        :Time complexity: O(M) where M is the length of the word
        :Aux space complexity: This is the space complexity of initializing a Node() object and storing the relevant data
                               such as the word, definition and frequency which takes up O(n+m) space
                               where n is the length of the word and m is the length of the definition.
        """
        # Begin from root
        current = self.root

        for char in word:
            index = ord(char) - 96
            # If path exists, traverse down the TRIE nodes
            if current.link[index] is not None:
                current = current.link[index]

            # If path doesn't exist, create a new node for that character in the string
            else:
                current.link[index] = Node(char)
                current = current.link[index]

        # When we have inserted the final node, place a terminal and store the definition and frequency
        current.terminal = True
        current.definition = definition
        current.frequency = frequency

    def prefix_search(self, prefix: str):
        """
        Function description:
        This function will take a prefix of a word and will search the TRIE structure for all words that match the prefix
        and will return a list containing a word that matches the prefix with the highest frequency in the dictionary,
        its definition and the total no.of words that match the prefix.

        Approach description:
        We begin by starting at the root node of the TRIE structure using a pointer and iteratively traverse down the
        nodes one character at a time until we have reached the node of the final character of the prefix.
        Once the pointer is pointing to the node of the last character in the prefix, we will begin the search for all
        words that match the prefix by recursively performing a Depth-first-search (DFS) traversal.

        During the DFS traversal, everytime we encounter a Terminal symbol in a node, we will increment a counter "count"
        that will keep track of the total no.of words that match the prefix.
        We will also check if the newly encountered terminal node has a frequency higher than the last word we found,
        and we will choose the new word as the result. The word with the highest frequency encountered during traversal
        will be the word displayed in the result along with its definition.

        The DFS traversal will simply update the result list as it performs a search for all words and once the traversal
        is complete, the final result list will be returned as output.

        :Input:
            argv1: Prefix string

        :Output, return or postcondition: A list [word with the highest freq, definition of word, total no of prefix-matching words]

        :Time complexity: Worst case time complexity of O(M+N) where M is length of the prefix and N is the total no.of nodes in the TRIE
        :Aux space complexity: O(1) because the only structure being created is the result list which is a constant size everytime.
        """
        current = self.root

        # Moving the pointer to the end of the prefix to begin search
        for char in prefix:  # O(M) time, where M is length of the prefix
            index = ord(char) - 96
            if current.link[index]:
                current = current.link[index]
            else:
                # If the prefix does not exist in the TRIE
                return [None, None, 0]

        # Initialize result
        result = [None, None, 0, 0]  # [word, definition, frequency, count]

        # Perform DFS traversal
        self.dfs_traversal(current, prefix, result)  # O(N) time, where N is the total no.of nodes in the TRIE
        result.remove(result[2])
        return result

    def dfs_traversal(self, node, prefix, result):
        """
        Function description:
        Recursively perform depth first search traversal on each node and update the result list as needed on every
        terminal encountered.

        :Input:
            argv1: Node
            argv1: Prefix string so far
            argv1: Result list so far

        :Output, return or postcondition: Final updated result list

        :Time complexity: The worst case that can happen is when we have all 26 alphabets a-z and for each alphabet,
                          there are 26 more children. The DFS will have to traverse EVERY SINGLE NODE in the TRIE
                          structure and so this can take O(N) time, where N is the total no.of nodes in the TRIE.

                          This can be improved to O(N) where N is the length of the word with the highest frequency
                          by adding an early termination but by also adding conditions for choosing which specific
                          child node to traverse down instead of iteratively traversing and checking each and every
                          child node which the code is currently doing.

        :Aux space complexity: O(1) since no new structures are being created.
        """
        if node.terminal:
            result[3] += 1
            if node.frequency > result[2]:
                result[0] = prefix
                result[1] = node.definition
                result[2] = node.frequency

        for i, child in enumerate(node.link):
            if child is not None:
                self.dfs_traversal(child, prefix + child.label, result)


if __name__ == "__main__":
    Dictionary = load_dictionary("Dictionary.txt")
    my_trie = Trie(Dictionary)
    print(my_trie.prefix_search(''))



