# 1. Generator that yields squares of numbers from 0 to N
def squares(n):
    for i in range(n + 1):
        yield i ** 2

n = int(input())
for square in squares(n):
    print(square)