#Write a Python program that matches a string that has an 'a' followed by two to three 'b'.

import re

pattern = r"ab{2,3}"
s = input("Enter a string: ")

if re.fullmatch(pattern, s):
    print("Match")
else:
    print("No match")
