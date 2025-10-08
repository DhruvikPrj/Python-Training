# fetch data from file
import pandas as pd

df = pd.read_csv("/Users/m1macmini3/Desktop/Python/PythonWeekTwo/Py-week-two/day2/students.csv")

def get_older_students(age_limit):
    """Returns list of students older than given age_limit"""
    return [name for name, age in zip(df["name"], df["age"]) if age > age_limit]

print("Students older than 18:", get_older_students(18))
print("Students older than 20:", get_older_students(20))

# Add new students to DataFrame
new_data = {"name": ["Anjali", "Vikram"], "age": [22, 15]}
new_df = pd.DataFrame(new_data)

# Append old + new
all_students = pd.concat([df, new_df], ignore_index=True)

# Save to new CSV
all_students.to_csv("students_updated.csv", index=False)

print("✅ students_updated.csv file created successfully!",all_students)

#Jab tu len(numbers) likhta hai → Python actually list object ke __len__ method ko call karta hai.
#Har Python object ke andar ek "dunder method" (double underscore method) hota hai.

#want to show library source code then:
# import inspect
# print(inspect.getsource(pd.read_csv))