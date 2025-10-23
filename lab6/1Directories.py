import os

path = input("Enter path: ")

print("Directories:")
for name in os.listdir(path):
    if os.path.isdir(os.path.join(path, name)):
        print(name)

print("Files:")
for name in os.listdir(path):
    if os.path.isfile(os.path.join(path, name)):
        print(name)

print("All:")
print(os.listdir(path))