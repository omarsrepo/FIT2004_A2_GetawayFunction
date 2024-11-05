from math import ceil


# DO NOT CHANGE THIS FUNCTION
def load_dictionary(filename):
    infile = open(filename)
    word, frequency = "", 0
    aList = []
    for line in infile:
        line.strip()
        if line[0:4] == "word":
            line = line.replace("word: ", "")
            line = line.strip()
            word = line
        elif line[0:4] == "freq":
            line = line.replace("frequency: ", "")
            frequency = int(line)
        elif line[0:4] == "defi":
            index = len(aList)
            line = line.replace("definition: ", "")
            definition = line.replace("\n", "")
            aList.append([word, definition, frequency])

    return aList


# Question 1
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

        self.edges = []

    def __repr__(self):
        return f"Vertex({self.label})"


class Edge:

    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.flow = 0
        self.capacity = w

    def __repr__(self):
        return f"Edge(u = {self.u}, v = {self.v}, flow = {self.flow}, capacity = {self.capacity})"


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
        result = [None, None, 0, 0]  # [word, definition, frequency, total count]

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
            result[3] += 1  # Update the total count everytime we find a word
            if node.frequency > result[2]:
                result[0] = prefix
                result[1] = node.definition
                result[2] = node.frequency

        for i, child in enumerate(node.link):
            if child is not None:
                self.dfs_traversal(child, prefix + child.label, result)


# Question 2

def allocate(preferences: list[list], licences: list):
    """
    Function description:
        This function will be used to compute one of many valid combinations of allocating people into
        cars for them to go on a trip while maintaining certain constraints.

    Approach description:
        1. We first calculate the total no.of people, the minimum no.of cars required and the shortlisted no.of destinations.
        2. We then check if we have enough drivers in the first place to make the trip.
           We need a minimum of 2 drivers per car which means if we have 3 cars, we need a minimum of 6 drivers and
           if we have 3 cars and only 5 drivers, we immediately return None saying that the trip is impossible to be made.
        3. Once we know that we have enough drivers, we will handle them by sorting the drivers into the cars based on their
           preferences of destinations. This is handled by the sort_driver() function below.
        4. Finally, one the drivers have been successfully allocated into the correct cars based on their preferences,
           we handle the remaining people who are not driving.
           We will find the people who are not driving by identifying their indexes as the indexes that are NOT part of the
           licenses list. Once we have identified them, we simply allocate them into a car with the least no.of people that
           is NOT FULL and also going to one of their preferred destinations. This way we will keep increasing the no.of
           members of each car simultaneously rather than filling one car up first and then moving to the next.

    :Input:
        argv1: preferences (list of lists indicating the destinations in which person i is interested.)
        argv2: licences (list indicating which persons have driver licences)
    :Output, return or postcondition:
        1: None ( if it is impossible to allocate the persons into the cars/destinations while satisfying all constraints.)
        2: cars (list of lists in which, for 0 ≤ j ≤ ⌈n/5⌉ − 1, cars[j] is a list identifying the persons that will be traveling on car j to destination j)

    :Time complexity:
        Best and Worst case of O(N^2)
        When we look for the remaining people who do not have licenses, we can potentially have the worst case of O(N^2)
        because the length of the licenses list can be as long as N.
        The bubble sort section in sort_drivers() function has the best and worst time complexity of O(N^2).
        Overall, the time complexity is dominated by bubble sorting in sort_drivers() -> Refer to documentation below.

        Is it
        """

    # We need to create the set of vertices for locations first
    # We also need to create a list of edges
    n = len(preferences)  # Number of people
    no_of_cars_or_destinations = ceil(n / 5)  # Number of available cars/destinations
    no_of_drivers_required = 2 * no_of_cars_or_destinations  # Number of drivers required

    # --------------------------------------------------------------------------- Creating the flow network ---------------------------------------------------------------------------
    source = Node('source')
    sink = Node('sink')
    set1 = []  # People set
    set2 = []  # Destination set

    for i in range(n):
        set1.append(Node(i + 1))
    for i in range(no_of_cars_or_destinations):
        node = Node(f'Destination{i}')
        set2.append(node)

    # Connect all the edges of the bipartite graph and connect people to destinations -> O(ND) where N = no.of people and D = no.of preferences per person and D << N
    for i in range(len(set1)):
        person = set1[i]
        source.edges.append(Edge(source, person, ceil(n / 5)))
        for persons_preference in preferences[i]:
            person.edges.append(Edge(person, set2[persons_preference], 1))

    for destination in set2:
        destination.edges.append(Edge(destination, sink, 5))

    # --------------------------------------------------------------------------- Creating the flow network ---------------------------------------------------------------------------

    return source, set1, set2


def allocate2(preferences: list[list], licences: list) -> list[list[int]] | None:
    """
    Function description:
        This function will be used to compute one of many valid combinations of allocating people into
        cars for them to go on a trip while maintaining certain constraints.

    Approach description:
        1. We first calculate the total no.of people, the minimum no.of cars required and the shortlisted no.of destinations.
        2. We then check if we have enough drivers in the first place to make the trip.
           We need a minimum of 2 drivers per car which means if we have 3 cars, we need a minimum of 6 drivers and
           if we have 3 cars and only 5 drivers, we immediately return None saying that the trip is impossible to be made.
        3. Once we know that we have enough drivers, we will handle them by sorting the drivers into the cars based on their
           preferences of destinations. This is handled by the sort_driver() function below.
        4. Finally, one the drivers have been successfully allocated into the correct cars based on their preferences,
           we handle the remaining people who are not driving.
           We will find the people who are not driving by identifying their indexes as the indexes that are NOT part of the
           licenses list. Once we have identified them, we simply allocate them into a car with the least no.of people that
           is NOT FULL and also going to one of their preferred destinations. This way we will keep increasing the no.of
           members of each car simultaneously rather than filling one car up first and then moving to the next.

    :Input:
        argv1: preferences (list of lists indicating the destinations in which person i is interested.)
        argv2: licences (list indicating which persons have driver licences)
    :Output, return or postcondition:
        1: None ( if it is impossible to allocate the persons into the cars/destinations while satisfying all constraints.)
        2: cars (list of lists in which, for 0 ≤ j ≤ ⌈n/5⌉ − 1, cars[j] is a list identifying the persons that will be traveling on car j to destination j)

    :Time complexity:
        Best and Worst case of O(N^2)
        When we look for the remaining people who do not have licenses, we can potentially have the worst case of O(N^2)
        because the length of the licenses list can be as long as N.
        The bubble sort section in sort_drivers() function has the best and worst time complexity of O(N^2).
        Overall, the time complexity is dominated by bubble sorting in sort_drivers() -> Refer to documentation below.

        Is it possible to improve this time complexity?
        Of course, by choosing a more optimal sorting algorithm such as Mergesort, QuickSort, Tim Sort, Heap sort etc.,
        or using a data structure that could provide a better search and sort time complexity. Fortunately, the worst
        time complexity requirement for this question was O(N^3) and bubble sort, while not being the best algorithm,
        is a simple enough sorting approach that adequately fits into the worst time complexity requirements for this
        question.

    :Aux space complexity:
        Aux space complexity is O(N) worst case
        Total Space complexity is O(N) worst case

        1. From sort_drivers() function, we have an Aux space complexity of O(N) worst case.
        2. Furthermore, we create one additional data structure in this function which is:
           people_without_licences -> Worst case of O(Y) where Y is the no.of people without licenses

        Aux space complexity = O(N) + O(Y) = O(N+Y) = O(N)
        Overall, the Auxiliary space complexity is dominated by the sort_drivers() function.

        Furthermore, the TOTAL space complexity is the space of the inputs + Aux space complexity
        inputs are:
            preferences = worst case O(N) where N is the no.of people
            licences = worst case O(N) where N is the no.of people
        Input + Aux = O(N+N) + O(N+Y) = O(N) + O(N+Y) = O(N) + O(N) = O(N)
        Total Space complexity = O(N) worst case
    """

    n = len(preferences)  # Number of people
    no_of_cars_or_destinations = ceil(n / 5)  # Number of available cars/destinations
    no_of_drivers_required = 2 * no_of_cars_or_destinations  # Number of drivers required

    # Base case to check if there are enough drivers
    if len(licences) < no_of_drivers_required:
        return None

    # We begin by sorting the drivers into the correct cars using sort_drivers() function
    cars = sort_drivers(preferences, licences)
    if not cars:
        return None

    # Find the remaining people who do not have licenses
    # Worst time complexity O(N^2) because everyone could potentially have a license (license list can be as long as N)
    people_without_licences = []
    for people in range(n):
        has_licence = False
        for driver in licences:
            if people == driver:
                has_licence = True
                break
        if not has_licence:
            people_without_licences.append(people)

    # Place the remaining people who are not driving into one of the cars they can go in
    for people in people_without_licences:
        people_preferences = preferences[people]
        if not people_preferences:  # Return None if a person has no preferences at all (Handling edge case)
            return None
        else:
            for dest in people_preferences:
                if dest < 0:
                    return None

        # If the person only has one preference, put them in that car
        # If the car is full, then look for someone in that car to swap with them. Return None if no swaps can be made
        if len(people_preferences) < 2:
            preference = people_preferences[0]
            if len(cars[preference]) < 5:
                cars[preference].append(people)
            else:
                for person_to_swap in cars[preference]:  # This loops for a maximum of 5 times
                    swap = False
                    persons_preference = preferences[person_to_swap]
                    if len(persons_preference) < 2:
                        continue
                    else:  # If the person we want to move has more than one preference, re-allocate them
                        for car in persons_preference:  # This loop will run a maximum of ceil(N/5) times
                            if car != preference:
                                if len(cars[car]) < 5:
                                    cars[car].append(person_to_swap)
                                    cars[preference].remove(person_to_swap)
                                    cars[preference].append(people)
                                    swap = True
                                    break
                    if swap:
                        break
                    else:
                        continue

                # If the car is full, and we couldn't make a swap, return None
                if not swap:
                    return None

        # If the person has more than one preference, put them in the least crowded car
        else:
            least_crowded = people_preferences[0]
            for i in people_preferences[1:]:
                if len(cars[i]) < len(cars[least_crowded]):
                    least_crowded = i
            if len(cars[least_crowded]) < 5:
                cars[least_crowded].append(people)
            else:
                for preference in people_preferences:
                    for person_to_swap in cars[preference]:  # This loops for a maximum of 5 times -> O(1)
                        swap = False
                        persons_preference = preferences[person_to_swap]
                        if len(persons_preference) < 2:
                            continue
                        else:  # If the person we want to move has more than one preference, re-allocate them
                            for car in persons_preference:  # This loop will run a maximum of ceil(N/5) times
                                if car != preference:
                                    if len(cars[car]) < 5:
                                        cars[car].append(person_to_swap)
                                        cars[preference].remove(person_to_swap)
                                        cars[preference].append(people)
                                        swap = True
                                        break
                            if swap:
                                break
                            else:
                                continue
                if swap:
                    break
                else:
                    return None

    return cars


def sort_drivers(preferences, licences):
    """
    Function description:
        This function will be used to compute one of many valid combinations of allocating people into
        cars for them to go on a trip while maintaining certain constraints such as

    :Input:
        argv1: preferences (list of lists indicating the destinations in which person i is interested.)
        argv2: licences (list indicating which persons have driver licences)
    :Output, return or postcondition:
        1: cars (list of lists in which, for 0 ≤ j ≤ ⌈n/5⌉ − 1, cars[j] is a list identifying the drivers that will be traveling on car j to destination j)

    :Time complexity:
        Best and Worst case of O(N^2)
        The time complexity is dominated by the bubble sort section that iterates through the list of drivers
        multiple times and has an overall best and worst time complexity of O(N^2) where N is the no.of drivers
        which can potentially be equal to the total no.of people in the case that everyone has a license.

    :Aux space complexity:
        Aux space complexity is O(N) worst case
        Total Space complexity is O(N) worst case

        We create three new arrays
        1. assigned_drivers -> Worst case of O(N) space where N is the total number of people
        2. cars -> Worst case O(m) space where m is derived from N and represents the number of available cars/destinations.
        3. preference_lengths -> Worst case of O(N) space where N is the total no.of people

        Aux space complexity = O(N+N+m)
        Overall, the Auxiliary space complexity is dominated by assigned_drivers and preference_lengths which can be
        O(N) in the worst case and therefore Aux space complexity is O(N)

        Furthermore, the TOTAL space complexity is the space of the inputs + Aux space complexity
        inputs are:
            preferences = worst case O(N) where N is the no.of people
            licences = worst case O(N) where N is the no.of people
        Input + Aux = O(N+N) + O(N+N+m) = O(N) + O(N+m) = O(N) + O(N) = O(N)
        Total Space complexity = O(N) worst case
    """
    driver_preferences = None
    n = len(preferences)  # Number of people
    m = ceil(n / 5)  # Number of available cars/destinations

    # Create a list to track assigned drivers
    assigned_drivers = [False] * n
    # Create cars with empty passenger lists
    cars = [[] for _ in range(m)]

    preference_lengths = [0] * len(licences)
    for i, driver_id in enumerate(licences):
        preference_lengths[i] = len(preferences[driver_id])

    # Sort drivers based on preferences using bubble sort
    # Worst Time Complexity of O(N^2) where N is the total no.of people (everyone may have a license)
    for i in range(len(licences) - 1):
        swapped = False
        for j in range(len(licences) - i - 1):
            if preference_lengths[j] > preference_lengths[j + 1]:
                licences[j], licences[j + 1] = licences[j + 1], licences[j]
                preference_lengths[j], preference_lengths[j + 1] = preference_lengths[j + 1], preference_lengths[j]
                swapped = True
        if not swapped:
            break

    for driver_id in licences:

        # Check if the driver has not been assigned yet
        if not assigned_drivers[driver_id]:
            driver_preferences = preferences[driver_id]
            if not driver_preferences:  # Accounting for a person having no preferences at all
                return None

        # If the driver only has one preference, put them in that car
        # Return None if the car is full
        if len(driver_preferences) < 2:
            preference = driver_preferences[0]
            if len(cars[preference]) < 5:
                cars[preference].append(driver_id)
                assigned_drivers[driver_id] = True
            else:
                return None

        # If the driver has more than one preference, find a car for the driver
        else:
            least_crowded = driver_preferences[0]
            for i in driver_preferences[1:]:
                if len(cars[i]) < len(cars[least_crowded]):
                    least_crowded = i
            cars[least_crowded].append(driver_id)
            assigned_drivers[driver_id] = True

    # Iterate through the cars and check if each car has at least 2 drivers
    # Return None if a car has less than 2 drivers
    for car in cars:
        if len(car) < 2:
            return None
    return cars


if __name__ == "__main__":
    # Dictionary = load_dictionary("Dictionary.txt")
    # my_trie = Trie(Dictionary)
    # print(my_trie.prefix_search(''))
    preferences = [[0], [1], [0, 1], [0, 1], [1, 0], [1], [1, 0], [0, 1], [1]]
    licences = [1, 4, 0, 5, 8]
    source, people, destination = allocate(preferences, licences)
    # print(f'Source = {source}')
    # print(f'People = {people}')
    # print(f'Destinations = {destination}')
    # print()
    #
    # for item in source.edges:
    #     print(item)
    # print()
    # for item in people:
    #     print(item.edges)
    # print()
    # for item in destination:
    #     print(item.edges)
    # for i, item in enumerate(licences):
    #     print(i)

    print(allocate2(preferences, licences))
