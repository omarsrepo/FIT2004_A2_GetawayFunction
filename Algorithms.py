import heapq


class MinHeap:
    """
    This is a class for a binary min-heap data structure.

    :Input: None
    :Output,return or post condition: None

    :Time complexity:
    ----------------------
    Best case of O(1) for certain operations and worst case of O(log n) for certain operations

    :Aux space complexity:
    ----------------------
    Best and worst case of O(1)

    :return: None
    """

    def __init__(self):  # O(1)
        self.heap = []

    def push(self, item):  # O(log n)
        heapq.heappush(self.heap, item)

    def pop(self):  # O(log n)
        if self.is_empty():
            raise IndexError("Heap is empty")
        return heapq.heappop(self.heap)

    def peek(self):  # O(1)
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.heap[0]

    def is_empty(self):  # O(1)
        return len(self.heap) == 0

    def size(self):  # O(1)
        return len(self.heap)

    def print_heap(self):
        if self.is_empty():
            print("Heap is empty")
            return

        def visualize(index, indent=""):
            if index < len(self.heap):
                print(indent + str(self.heap[index]))
                left_child = 2 * index + 1
                right_child = 2 * index + 2
                if left_child < len(self.heap):
                    visualize(left_child, indent + "  |__ ")
                if right_child < len(self.heap):
                    visualize(right_child, indent + "  |__ ")

        visualize(0)


def bfs_shortest_paths(discovered: MinHeap):
    # We will assume that the graph is represented using an adjacency list
    # Input "u" is the parent vertex
    # BFS algorithm incorporates the use of a MinHeap queue
    while not discovered.is_empty():
        u = discovered.pop()
        u.visited = True
        for child in u.edges:
            if not child.discovered:
                child.distance += u.distance + 1
                child.previous = u
                discovered.push(child)
            elif not child.visited:
                # Update the child's distance if they have been discovered
                if child.discovered > u.distance + 1:
                    child.discovered = u.distance + 1
                    child.previous = u
    return


def insertion_sort(array: list):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1  # Move the pointer to the next element to the left and compare again
        array[j + 1] = key

    return array


def selection_sort(array: list):
    for i in range(0, len(array)):
        minimum = i
        for j in range(i + 1, len(array)):
            if array[j] < array[minimum]:
                minimum = j

        array[i], array[minimum] = array[minimum], array[i]

    return array


def counting_sort_stable(array: list):
    # Finding max value in list
    max = 0
    for item in array:
        if item > max:
            max = item

    # Create count array of size max
    count = [None] * (max + 1)
    for i in range(len(count)):
        count[i] = []

    # Count frequency of each value in array
    for item in array:
        count[item].append(item)

    # Updating the original array from count array
    array = []
    for item in count:
        if item:
            for j in item:
                array.append(j)

    return array


def quicksort_hoare(array: list):
    # In place version of quicksort

    # Find a random pivot
    low = 0
    hi = len(array)
    pivot = array[(low + hi) // 2]

    # Swap pivot to beginning of array
    array[(low + hi) // 2], array[0] = array[0], array[(low + hi) // 2]

    # Initialize two new pointers
    l_bad = 1
    r_bad = len(array) - 1

    while True:
        # Loop l_bad until we find a value greater than pivot
        while array[l_bad] <= pivot:
            l_bad += 1

        while array[r_bad] > pivot:  # Loop r_bad until we find a value smaller than pivot
            r_bad -= 1

        if r_bad < l_bad:
            return array
        else:
            # Perform a swap
            array[l_bad], array[r_bad] = array[r_bad], array[l_bad]

        quicksort_hoare(array)


# Quick sort in Python

# function to find the partition position
def partition(array, low, high):
    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
            # if element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # return the position from where partition is done
    return i + 1


# function to perform quicksort
def quickSort(array, low, high):
    if low < high:
        # find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # recursive call on the left of pivot
        quickSort(array, low, pi - 1)

        # recursive call on the right of pivot
        quickSort(array, pi + 1, high)


# data = [8, 7, 2, 1, 0, 9, 6]
# print("Unsorted Array")
# print(data)
#
# size = len(data)
#
# partition(data, 0, size - 1)
# print(data)
# partition(data, 0, size - 1)
# print(data)
unsorted = [2, 8, 7, 1, 3, 4, 5, 4]


print(4329 % 1000)