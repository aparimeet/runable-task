import os
import shutil

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)
    return f"File created at {path}"

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def update_file(path, content):
    with open(path, "a") as f:
        f.write(content)
    return f"File updated at {path}"

def move_file(src, dest):
    shutil.move(src, dest)
    return f"Moved {src} to {dest}"

def delete_file(path):
    os.remove(path)
    return f"Deleted file at {path}" 