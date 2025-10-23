def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

text = "Hello World"
u, l = count_case(text)
print(f"Upper case: {u}, Lower case: {l}")