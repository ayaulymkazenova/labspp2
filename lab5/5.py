#Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re

pattern = r"a.*b"
s = input("Enter a string: ")

if re.fullmatch(pattern, s):
    print("Match")
else:
    print("No match")
