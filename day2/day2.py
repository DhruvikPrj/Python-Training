# Text data ko handle karne ke liye.

name = "DCENT"
print(name.upper())   # DCENT
print(name.lower())   # dcent
print("  hi  ".strip())        # "hi"   (remove whitespace)
print("a,b,c".split(","))      # ['a','b','c']
print("-".join(["a","b","c"])) # "a-b-c"
print(name[0])        # D (indexing)
print(name[1:4])      # CEN (slicing)

# f-strings (most readable formatting):
name = "Aman"; age = 20
print(f"{name} is {age} years old")   # Aman is 20 years old

# Lists
# Ordered, changeable collection (like array).
students = ["Aman", "Ravi", "Sita"]
students.append("Neha")     # add item
print(students)             # ['Aman', 'Ravi', 'Sita', 'Neha']
print(students[1])          # Ravi

lst = [1, 2, 3]
lst.append(4)          # [1,2,3,4]
lst.extend([5,6])      # [1,2,3,4,5,6]
lst.insert(0, 0)       # [0,1,2,3,4,5,6]
print(lst[2])          # 2
print(lst[1:4])        # slice

lst.remove(3)          # remove first occurrence of 3
x = lst.pop()          # pop last element, returns value

a = [1,2,3]
b = a                  # b references same list (alias)
b.append(4)
print(a)               # [1,2,3,4]  <-- a changed too

c = a.copy()           # shallow copy, independent list

# Tuples
# 👉 Ordered but immutable (cannot change).
coordinates = (10, 20)
print(coordinates[1])   # 20

# Sets
# 👉 Unordered, unique values only.
numbers = {1, 2, 2, 3, 4}
print(numbers)     # {1, 2, 3, 4} (duplicates removed)

s = {1, 2, 2, 3}
print(s)                  # {1,2,3}

# Set operations
a = {1,2,3}
b = {3,4}
print(a | b)  # union {1,2,3,4}
print(a & b)  # intersection {3}
print(a - b)  # difference {1,2}
print(2 in a) # True  (O(1) avg)


# Dictionaries (Dicts)
# 👉 Key-value pairs (JSON jaisa).
student = {"name": "Aman", "age": 20}
print(student["name"])   # Aman
student["age"] = 21      # update
print(student)

d = {"name": "Aman", "age": 20}
print(d["name"])         # Aman
print(d.get("age"))      # 20
print(d.get("city", "unknown"))  # default if key missing

# iterate
for k, v in d.items():
    print(k, v)

# List Comprehension
# 👉 Short way to create lists.

numbers = [x for x in range(10)]   # [0,1,2,...,9]
squares = [x*x for x in range(5)]  # [0,1,4,9,16]

# Lambda Functions
# 👉 Small anonymous function.
square = lambda x: x * x
print(square(5))   # 25

# Looping
# 👉 Repeat actions.
students = ["Aman", "Ravi", "Sita"]
for s in students:
    print(s)

# Equivalent loop → comprehension:

# loop version
res = []
for x in range(10):
    if x % 2 == 0:
        res.append(x*x)

# comprehension version
res = [x*x for x in range(10) if x % 2 == 0]

# enumerate — index + value
for idx, val in enumerate(["a","b","c"], start=1):
    print(idx, val)   # 1 a ; 2 b ; 3 c

# zip — iterate multiple iterables in parallel
names = ["Aman","Ravi"]
ages  = [17, 20]
for n, a in zip(names, ages):
    print(n, a)

# Iterating dicts
d = {"a":1, "b":2}
for key in d:               # iterates keys
    print(key)
for k, v in d.items():      # iterate pairs
    print(k, v)

# range() for numeric loops
for i in range(5):  # 0..4
    print(i)

# while loop
i = 0
while i < 5:
    print(i)
    i += 1

# transform a list
names = ["Aman","Ravi","Sita"]
upper = [n.upper() for n in names]     # ['AMAN', 'RAVI', 'SITA']

# nested comprehension (matrix flatten)
matrix = [[1,2],[3,4]]
flat = [num for row in matrix for num in row]   # [1,2,3,4]


#================= Useful idioms & tips ================

# Unpacking
a, b, *rest = [1,2,3,4]   # a=1, b=2, rest=[3,4]

# Swap values
a, b = b, a

# Check membership
if "Aman" in names: ...

# Sort with key
people = [{"name":"A","age":20}, {"name":"B","age":18}]
people_sorted = sorted(people, key=lambda p: p["age"])

# Don’t modify a list while iterating it — use a new list or iterate a copy:

# Mutable default args (common pitfall):

def f(a, items=[]):   # BAD
    items.append(a)
    return items

# Use:
def f(a, items=None):
    if items is None:
        items = []




