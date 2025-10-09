# 3. Generator for numbers divisible by both 3 and 4 (i.e., by 12) in range 0 to n
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

n = int(input())
for num in divisible_by_3_and_4(n):
    print(num)