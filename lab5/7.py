#Write a python program to convert snake case string to camel case string.
import re

s = input("Enter a snake_case string: ")
parts = s.split('_')
camel = parts[0] + ''.join(word.title() for word in parts[1:])
print(camel)
