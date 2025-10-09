# 2. Print even numbers between 0 and n
n = int(input())
even_numbers = (str(i) for i in range(0, n + 1, 2))
print(','.join(even_numbers))