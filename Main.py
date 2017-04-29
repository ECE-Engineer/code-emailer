import os
import glob
import sys
from os.path import join
import filecmp
import shutil
import fnmatch

path = 'C:\\Users\\##########\\Desktop\\Courses\\344'
directory = 'C:\\Users\\##########\\Desktop\\csc344'
dir1 = 'C:\\Users\\##########\\Desktop\\csc344\\hw1'
dir2 = 'C:\\Users\\##########\\Desktop\\csc344\\hw2'
dir3 = 'C:\\Users\\##########\\Desktop\\csc344\\hw3'
dir4 = 'C:\\Users\\##########\\Desktop\\csc344\\hw4'

if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(dir1):
    os.makedirs(dir1)
if not os.path.exists(dir2):
    os.makedirs(dir2)
if not os.path.exists(dir3):
    os.makedirs(dir3)
if not os.path.exists(dir4):
    os.makedirs(dir4)

def copydir(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

# find all the src folders
for root, dirs, files in os.walk(path):
	for dir in dirs:
		newpath = os.path.join(root,dir)
		if filecmp.dircmp(dir, 'src'):
			# determine the file extensions of the files found to determine which folder to copy them to
			for file in files:
				somefile = file.rsplit('.', 1)[0]
				if somefile == 'main' and (file.endswith(".c") or file.endswith(".o")):
					copydir(root, dir1)
					break
				elif file.endswith(".clj"):
					copydir(newpath, dir2)
					break
				elif file.endswith(".hs"):
					copydir(newpath, dir3)
					break
				elif file.endswith(".pl"):
					copydir(newpath, dir4)
					break
print ('DONE!!!')