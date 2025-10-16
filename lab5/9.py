#Write a Python program to insert spaces between words starting with capital letters.
import re

s = input("Enter a string: ")
result = re.sub(r"(?=[A-Z])", " ", s).strip()
print(result)
