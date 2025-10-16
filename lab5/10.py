#Write a Python program to convert a given camel case string to snake case.
import re

s = input("Enter a camelCase string: ")
result = re.sub(r"([A-Z])", r"_\1", s).lower()
print(result)
