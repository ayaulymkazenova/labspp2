from functools import reduce
import operator

def multiply_list(numbers):
    return reduce(operator.mul, numbers) if numbers else 0


print(multiply_list([1, 2, 3, 4, 5]))  