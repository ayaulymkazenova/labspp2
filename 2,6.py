
def reverse_sentence(s):
    return ' '.join(s.split()[::-1])

s = input()
print(reverse_sentence(s))
