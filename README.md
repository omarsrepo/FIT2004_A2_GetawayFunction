# FIT2004 Assignment 2 Question 2
**A Weekend Getaway (10 marks)**
With the end of the semester rapidly approaching, you and most of your friends realised that a weekend getaway after Week 12 would be a great idea so that you relax a bit before starting studying for your final exams. The ones that were not initially sure if taking 2 days off would be best idea eventually decided to go with the flow and also plan a weekend getaway.
You all got excited and came up with great ideas for destinations nearby, but soon realised that there are some constraints:
1. You want to save money and therefore you want to use the least amount of cars possible.
2. Not all of you have driver licences.
3. People have different preferences regarding destinations, and everyone should go to one of the locations they want.
4. You are all very tired after Week 12 and therefore agreed that no one should be the driver on both the outbound and inbound journeys.
After some discussions you come up with the following agreement:
• You realised that each car available can transport up to 5 people (including the driver). As you are n persons, you decided to use ⌈n/5⌉ cars in order to reduce the costs (and you have ⌈n/5⌉ cars available).
• You shortlisted ⌈n/5⌉ different destinations. For each of those destinations, one car will be going there with up to 5 persons on it, and the car will stay on that destination for the whole weekend (i.e., it is not possible to reuse the car to bring more people).
• Everyone will indicate the destinations they are interested in and if they have a driver licence or not.
• Everyone should be going to one of the destinations they are interested in (and only the ⌈n/5⌉ cars can be used as means of transport).
• In every car there should be at least two persons with driver licences traveling on it, so that the driver on the inbound journey is not the same as the driver in the outbound journey.
As the computer scientist in the group, you were tasked with writing a computer program to: either find a way to divide the persons into the cars/destinations so that all the above constraints are satisfied; or correctly indicate it is impossible to divide the persons into the cars/destinations while satisfying all constraints.
The persons will be numbered 0, 1, . . . , n − 1, while the destinations/cars will be numbered 0, 1, . . . , ⌈n/5⌉ − 1. Car number j will go to the destination number j. You will get as input a list of lists preferences and a list licences such that:
• For each 0 ≤ i ≤ n − 1, the elements of the list preferences[i] will form a subset of {0, 1, . . . , ⌈n/5⌉ − 1} indicating the destinations in which person i is interested. You cannot assume that the elements in preferences[i] are listed in any specific order.
9
• The elements of the list licences will form a subset of {0, 1, . . . , n − 1} indicating which persons have driver licences. You cannot assume that the elements in licences are listed in any specific order.
To solve this problem, you should write a function allocate(preferences, licences) that returns:
• None (i.e., Python NoneType), if it is impossible to allocate the persons into the cars/des- tinations while satisfying all constraints.
• Otherwise, it returns a list of lists cars in which, for 0 ≤ j ≤ ⌈n/5⌉ − 1, cars[j] is a list identifying the persons that will be traveling on car j to destination j. If there are multiple valid allocations satisfying all constraints, you can return any of those valid allocations (but should return exactly one of them).
