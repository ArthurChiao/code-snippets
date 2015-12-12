
import os

def list_content(path):
    """
    list all files of given dir, recursively into subdirs
    """
    for f in os.listdir(path):
        subdir = os.path.join(path, f)
        if os.path.isdir(f):
            list_content(subdir)
        else:
            print f

if __name__ == '__main__':
    list_content("/home/arthur/")
