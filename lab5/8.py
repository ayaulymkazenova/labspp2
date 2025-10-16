#Write a Python program to split a string at uppercase letters.
import re

s = input("Enter a string: ")
result = re.split(r"(?=[A-Z])", s)
print(result)
