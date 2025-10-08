# File Handling with open()
# Python me files handle karne ke liye open() function use hota hai.
# Modes (second argument of open()):

# 'r'         open for reading (default)

# 'w'        open for writing, truncating the file first

# 'x'        create a new file and open it for writing

# 'a'        open for writing, appending to the end of the file if it exists

# 'b'        binary mode

# 't'        text mode (default)

# '+'        open a disk file for updating (reading and writing

# with ... as f: automatically file close() kar deta hai (best practice).

# Write to a file
with open("notes.txt", "w") as f:
    f.write("Hello DCENT!\n")
    f.write("Python file is created and written...\n")

# Read the file
with open("notes.txt", "r") as f:
    content = f.read()
    print("File Content:\n", content)


# JSON with json module
# JSON (JavaScript Object Notation) ek text-based format hai data exchange ke liye (API, config files, etc.).

import json

# Python dict → JSON (write to file)
data = {"name": "Dhruvik", "age": 20, "city": "Ahmedabad"}
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)   # indent = pretty format

# JSON file → Python dict (read)
with open("data.json", "r") as f:
    loaded = json.load(f)
    print(loaded)         # {'name': 'Aman', 'age': 20, 'city': 'Delhi'}

# directly string ↔ dict:

    s = '{"name":"Ravi","age":25}'
    print(json.loads(s))  # string → dict
    print(json.dumps({"x": 1}))  # dict → string

# Requests for API Calls
# We’ll use requests library to call web APIs.

import requests

response = requests.get("https://fakestoreapi.com/products")
print("Status:", response.status_code)    # 200 = success
print("Response JSON:", response.json())  # [{'id': 1, 'title': 'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops', 'price': 109.95, ...}]


# Error Handling with try-except
try:
    with open("notes.txt", "r") as f:
        print("Read by Me:::",f.read())
except FileNotFoundError:
    print("File not found!")

try:
    r = requests.get("https://httpbin.org/status/404")
    r.raise_for_status()   # throws error if status != 200
except requests.exceptions.RequestException as e:
    print("API error:", e)
