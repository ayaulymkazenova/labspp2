#Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re

pattern = r"[A-Z][a-z]+"
s = input("Enter a string: ")

if re.fullmatch(pattern, s):
    print("Match")
else:
    print("No match")
