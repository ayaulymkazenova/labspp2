#Write a Python program to find sequences of lowercase letters joined with a underscore.
import re

pattern = r"[a-z]+_[a-z]+"
s = input("Enter a string: ")

if re.fullmatch(pattern, s):
    print("Match")
else:
    print("No match")
