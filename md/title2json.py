import os
cwd = os.getcwd()
tups = os.walk(cwd)
for root, dirs, files in tups:
    print(root, dirs, files)