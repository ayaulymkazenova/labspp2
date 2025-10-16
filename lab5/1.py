#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re

pattern = r"ab*"
s = input("Enter a string: ")
if re.fullmatch(pattern, s):
    print("Match")
else:
    print("No match")
