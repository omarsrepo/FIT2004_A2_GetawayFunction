from math import ceil


def allocate(preferences, licences):
    cars = sort_drivers(preferences, licences)
    if cars is None:
        return cars

    # Find the remaining people who do not have licenses
    no_of_people = len(preferences)
    people_without_licences = []

    # Worst time complexity O(N+M) where N = Total people and M = People with licences
    for people in range(no_of_people):
        has_licence = False
        for driver in licences:
            if people == driver:
                has_licence = True
                break
        if not has_licence:
            people_without_licences.append(people)
    print(f'People without licenses: {people_without_licences} ------- from allocate()\n')

    # Worst time complexity O(M+m) where M = People with licences and m = no.of cars or destinations
    for people in people_without_licences:

        people_preferences = preferences[people]
        if not people_preferences:  # Accounting for a person having no preferences at all
            return None

        if len(people_preferences) < 2:  # If the person only has one preference, put them in that car
            for j in range(m):
                if len(cars[j]) < 5:
                    if j in people_preferences:
                        cars[j].append(people)
                        break
        else:  # If the person has more than one preference, find a car for the person
            least_crowded = people_preferences[0]
            for i in people_preferences[1:]:
                if len(cars[i]) < len(cars[least_crowded]):
                    least_crowded = i
            if len(cars[least_crowded]) < 5:
                cars[least_crowded].append(people)

    return cars


def sort_drivers(preferences, licences):
    driver_preferences = None
    n = len(preferences)  # Number of people
    m = ceil(n / 5)  # Number of available cars/destinations
    no_of_drivers_required = 2 * m  # Number of drivers required

    # Create a list to track assigned drivers
    assigned_drivers = [False] * n

    # Create cars with empty passenger lists
    cars = [[] for _ in range(m)]

    if len(licences) < no_of_drivers_required:
        return None
    else:
        # Sort drivers based on the number of preferences (ascending)
        # licences.sort(key=lambda driver_idx: len(preferences[driver_idx]))
        # print(f'Sorted licenses: {licences} ------- from sort_drivers()')

        # Sort drivers based on preferences using bubble sort
        # Worst Time Complexity of O(N^2) where N is the number of people with licenses
        preference_lengths = [0] * len(licences)
        for i, driver_id in enumerate(licences):
            preference_lengths[i] = len(preferences_list[driver_id])

        for i in range(len(licences) - 1):
            swapped = False
            for j in range(len(licences) - i - 1):
                if preference_lengths[j] > preference_lengths[j + 1]:
                    licences[j], licences[j + 1] = licences[j + 1], licences[j]
                    preference_lengths[j], preference_lengths[j + 1] = preference_lengths[j + 1], preference_lengths[j]
                    swapped = True
            if not swapped:
                break
        print(f'Sorted license: {licences} ------- from sort_drivers()')

        for driver_id in licences:

            # Check if the driver has not been assigned yet
            if not assigned_drivers[driver_id]:
                driver_preferences = preferences[driver_id]
                if not driver_preferences:  # Accounting for a person having no preferences at all
                    return None

            if len(driver_preferences) < 2:  # If the driver only has one preference, put them in that car
                for j in range(m):
                    if len(cars[j]) < 5:
                        if j in driver_preferences:
                            cars[j].append(driver_id)
                            assigned_drivers[driver_id] = True
                            break
            else:  # If the driver has more than one preference, find a car for the driver
                least_crowded = driver_preferences[0]
                for i in driver_preferences[1:]:
                    if len(cars[i]) < len(cars[least_crowded]):
                        least_crowded = i
                cars[least_crowded].append(driver_id)
                assigned_drivers[driver_id] = True

        return cars


# Example usage:
preferences_list = [[0], [1, 2], [0, 1, 2], [0, 1], [1, 0], [1], [1, 0], [0, 1], [1], [2], [2, 1], [0, 2]]
licences = [1, 4, 0, 2, 5, 11]

n = len(preferences_list)  # No.of people
m = ceil(n / 5)  # Number of available cars/destinations
no_of_drivers_required = 2 * ceil(n / 5)  # Number of drivers required
cars = [[] for _ in range(m)]
print(f'Number of people: {n}')
print(f'Number of cars/destinations: {m}')
print(f'Number of drivers required: {no_of_drivers_required}')
print(f'Cars: {cars}\n')
print(allocate(preferences_list, licences))
