from math import ceil


def allocate(preferences: list[list], licences: list) -> list[list[int]] | None:
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
        print('Not enough drivers')
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
    print(f'People without licenses: {people_without_licences} ------- from allocate()\n')

    # Place the remaining people who are not driving into one of the cars they can go in
    for people in people_without_licences:
        people_preferences = preferences[people]
        if not people_preferences:  # Return None if a person has no preferences at all (Handling edge case)
            return None
        else:
            for dest in people_preferences:
                if dest < 0:
                    print(f'Person {people} has an invalid destination')
                    return None

        print(f'Cars list so far: {cars}')
        print(f'we are currently trying to allocate person {people} and their preferences are {people_preferences}\n')

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

                # print(f'\nCar {preference} is full and person {people} cannot fit in the car')
                # return None

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

    print(f'Cars list so far: {cars}\n')
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
    # print(f'Driver preferences: {preference_lengths} ------- from sort_drivers()')
    # print(f'Sorted license: {licences} ------- from sort_drivers()')

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

    print(f'Drivers in cars: {cars} ------- from sort_drivers()')
    # Iterate through the cars and check if each car has at least 2 drivers
    # Return None if a car has less than 2 drivers
    for car in cars:
        if len(car) < 2:
            print('Some car has less than 2 drivers')
            return None
    return cars


if __name__ == "__main__":
    import random

    def generate_random_preferences(n, m):
        preferences = []
        for _ in range(n):
            num_preferences = random.randint(1, m)  # Random number of preferences between 1 and m
            unique_preferences = random.sample(range(m), num_preferences)  # Sample unique values from 0 to m-1
            preferences.append(unique_preferences)
        return preferences

    def generate_random_licenses(n):
        # Generate a list of unique driver IDs ranging from 0 to no_of_people - 1
        driver_ids = list(range(n))
        random.shuffle(driver_ids)  # Shuffle the list to make it random
        num_licenses = random.randint(1, n)  # Random number of licenses between 1 and no_of_people
        licenses = driver_ids[:num_licenses]  # Select the first num_licenses IDs
        return licenses

    def generate_minimum_licenses(n):
        # Generate a list of unique driver IDs ranging from 0 to no_of_people - 1
        driver_ids = list(range(n))
        random.shuffle(driver_ids)  # Shuffle the list to make it random
        num_licenses = 2 * ceil(n / 5)  # Random number of licenses
        licenses = driver_ids[:num_licenses]  # Select the first num_licenses IDs
        return licenses


    no_of_people = random.randint(1, 25)
    m = ceil(no_of_people / 5)  # Number of available cars/destinations
    no_of_drivers_required = 2 * ceil(no_of_people / 5)  # Number of drivers required
    cars = [[] for _ in range(m)]

    preferences = generate_random_preferences(no_of_people, m)
    licences = generate_random_licenses(no_of_people)

    # preferences = [[2, 3, 1], [3, 0], [3, 2], [1, 0, 3, 2], [1, 3], [0, 2], [0, 1, 2], [2, 0, 1], [3, 0, 2], [2, 3],
    #                [3, 2], [3], [3, 1, 2], [1], [2, 0, 3], [2], [1], [1, 3], [2], [3, 1]]
    # licences = [14, 19, 8, 16, 13, 10, 17, 5, 11, 7, 2, 3, 0]
    print(f'preferences = {preferences}')
    print(f'licences = {licences}')
    print(f'Number of people: {len(preferences)}')
    print(f'Number of cars/destinations: {ceil( len(preferences) / 5 )}')
    print(f'Number of drivers required: {2 * ceil( len(preferences) / 5)}')
    print(f'Cars: {cars}\n')
    print('Output:')
    print(allocate(preferences, licences))
