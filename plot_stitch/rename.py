import os

for root, dirs, files in os.walk("剪裁"):
    for file in files:
        file_abs = os.path.join(root, file)
        newfile = None
        if file.startswith("E"):
            newfile = "5.png"
        elif file.startswith("M"):
            newfile = "3.png"
        elif file.startswith("T"):
            newfile = "4.png"
        elif file.startswith("710"):
            newfile = "6.png"
        elif file.startswith("A"):
            newfile = "7.png"
        if newfile is None:
            continue
        os.rename(file_abs, os.path.join(root, newfile))
