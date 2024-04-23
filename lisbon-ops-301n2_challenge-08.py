#!/usr/bin/python3

# Assigning a list of ten string elements to a variable
list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

# Printing the fourth element of the list (indexing starts from 0)
print("4th on the list:", list[3])

# Printing the sixth through tenth element of the list
print("6th through 10th on the list:", list[5:])

# Changing the value of the seventh element to "onion"
list[6] = "onion"

# Printing the updated list to verify the change
print("Onionized:", list)

# Stretch goals
print("\n")
print("Stretch goals")
print("\n")

# append() "42" to the list
list.append("42")
print("List after append:", list)
print("\n")

# clear() the list
list.clear()
list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] # Undoing clear() for next stretch goal

# copy() list into a new variable called "list_2"
list_2 = list.copy()
print("List 2: Electric Boogaloo:", list_2)
print("\n")

# count() number of specified element
three_count = list.count("3")
print("Count of '3':", three_count)
print("\n")

# extend() newly listed elements to list
extend_list = ["ext1", "ext2"]
list.extend(extend_list)
print("Extension:", list)
print("\n")

# index() something in the ilst
index_3 = list.index("3")
print("2 is indexed at:", index_3)
print("\n")

# insert() "W" into an element
list.insert(5, "W")
print("Inserted W:", list)
print("\n")

# pop() last element on the list
last_pop = list.pop()
print("Poppy:", last_pop)
print("\n")
list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] # Undoing clear() for next stretch goal

# remove() specified element from list (grape)
list.remove("4")
print("Removed 4:", list)
print("\n")

# reverse() the current order
list.reverse()
print("esreveR:", list)
print("\n")

# sort() list in alphabetical order
list = ["elephant", "guitar", "sunshine", "chocolate", "rainbow", "butterfly", "ocean", "mountain", "happiness", "adventure"]
list.sort()
print("Sorted word list:", list) 