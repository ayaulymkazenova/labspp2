src = input("Source file: ")
dest = input("Destination file: ")

with open(src, 'r') as f1, open(dest, 'w') as f2:
    f2.write(f1.read())