mylist = ["apple", "banana", "cherry"]
filename = input("Enter file name: ")

with open(filename, 'w') as f:
    for item in mylist:
        f.write(item + "\n")