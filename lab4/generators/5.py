# 5. Generator that returns numbers from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())
for num in countdown(n):
    print(num)