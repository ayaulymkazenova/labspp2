def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if 2 * chickens + 4 * rabbits == numlegs:
            return (chickens, rabbits)
    return (None, None)

numheads = 35
numlegs = 94
chickens, rabbits = solve(numheads, numlegs)
print(chickens, rabbits)