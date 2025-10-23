import os

path = input("Enter file path to delete: ")

if os.path.exists(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted")
    else:
        print("File not writable")
else:
    print("File does not exist")