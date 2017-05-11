import os
import glob
import sys
from os.path import join
from os import listdir
from os.path import isfile
import filecmp
import shutil
import fnmatch
import re
import webbrowser
from zipfile import ZipFile

### IMPORTANT THINGS TO KEEP IN MIND
# INTERESTING issues that using the walk function can cause,
# includes the fact that the program will never see the nested src folder,
# if the src folder per se does NOT also contain ANY ARBITRARY folder!!!



path = 'C:\\Users\\XXXXXXXXXX\\Desktop\\Courses\\344'
directory = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344'
dir1 = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\hw1'
dir2 = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\hw2'
dir3 = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\hw3'
dir4 = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\hw4'
dir5 = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\hw5'


rootDir = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344'
symbolsFileName = "symbols.txt"




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
if not os.path.exists(dir5):
    os.makedirs(dir5)

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
				elif somefile == 'Main' and file.endswith(".py"):
					copydir(root, dir5)
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





def zipFiles():
    zipRoot = os.path.basename(rootDir)
    with ZipFile(zipRoot + ".zip", 'w') as zipFile:
        zipFile.write(rootDir, zipRoot)
        for path, dirs, files in os.walk(rootDir):
            for file in files:
                fileName = os.path.basename(file)
                relPath = os.path.relpath(path, rootDir)
                src = os.path.join(path, file)
                dest = os.path.normpath(os.path.join(zipRoot, relPath, fileName))
                zipFile.write(src, dest)

def buildSymbolsFile():
    stream = createSymbolsFile()
    for dirName in os.listdir(rootDir):
        path = rootDir + "\\" + dirName
        if (os.path.isdir(path)):
            extractSymbolsToFile(stream, path)
    stream.close()

def createSymbolsFile():
    stream = open(rootDir + "\\" + symbolsFileName, "a+")
    stream.seek(0)
    stream.truncate()
    return stream

def extractSymbolsToFile(stream, filePath):
    for fileName in os.listdir(filePath):
        file = createSourceFile(fileName)
        symbols = file.extractSymbols()
        appendSymbolsToFile(stream, file, file.extractSymbols())

def appendSymbolsToFile(stream, sourceFile, symbols):
    for symbol in symbols:
        stream.write("[" + sourceFile.programName + ", " + symbol + "]\n")

def createSourceFile(fileName):
    if fileName.endswith(C_File.extension):
        return C_File(fileName)
    elif fileName.endswith(C_HeaderFile.extension):
        return C_HeaderFile(fileName)
    elif fileName.endswith(ClojureFile.extension):
        return ClojureFile(fileName)
    elif fileName.endswith(HaskellFile.extension):
        return HaskellFile(fileName)
    elif fileName.endswith(PrologFile.extension):
        return PrologFile(fileName)
    elif fileName.endswith(PythonFile.extension):
        return PythonFile(fileName)
    else:
        raise ValueError("Invalid file extension")

class SourceFile():
    extension = ""
    regexes = ""
    path = "C:\\Users\\S\\Desktop\\csc344"
    directory = ""
    quotedStringRegex = "(?:\".*?\")|(?:\'.*?\')"
    programName = ""

    def __init__(self, name):
        self.name = name
        self.fullPath = SourceFile.path + self.directory + "\\" + name
        stream = open(self.fullPath)
        self.text = stream.read()
        stream.close()

    def extractSymbols(self):
        regex = self.commentRegex + "|" + self.quotedStringRegex + "|" + self.identifierRegex
        symbols = set(re.findall(regex, self.text))
        symbols.discard('')
        return symbols

class C_File(SourceFile):
    extension = ".c"
    directory = "\\hw1"
    commentRegex = "(?://+.*(?:\n|$))|(?:\*+.*(?:\n|$))|(?:#+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z_]+[a-zA-Z0-9_]*)"
    programName = "C"

class C_HeaderFile(SourceFile):
    extension = ".h"
    directory = "\\hw1"
    commentRegex = "(?://+.*(?:\n|$))|(?:\*+.*(?:\n|$))|(?:#+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z_]+[a-zA-Z0-9_]*)"
    programName = "C"

class ClojureFile(SourceFile):
    extension = ".clj"
    directory = "\\hw2"
    commentRegex = "(?:;+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z]+[a-zA-Z0-9_?-]*)"
    programName = "Clojure"

class HaskellFile(SourceFile):
    extension = ".hs"
    directory = "\\hw3"
    commentRegex = "(?:--+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z]+[a-zA-Z0-9_']*)"
    programName = "Haskell"

class PrologFile(SourceFile):
    extension = ".pl"
    directory = "\\hw4"
    commentRegex = "(?:%+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z]+[a-zA-Z0-9_]*)"
    programName = "Prolog"

class PythonFile(SourceFile):
    extension = ".py"
    directory = "\\hw5"
    commentRegex = "(?:#+.*(?:\n|$))"
    identifierRegex = "([a-zA-Z]+[a-zA-Z0-9_]*[a-zA-Z]+)"
    programName = "Python"







c_files = [f for f in listdir(dir1) if (isfile(join(dir1, f))  and not f.endswith(".o"))]
clojure_files = [f for f in listdir(dir2) if (isfile(join(dir2, f)) and f.endswith(".clj"))]
haskell_files = [f for f in listdir(dir3) if (isfile(join(dir3, f)) and (f.rsplit('.', 1)[0] == 'Lib') and f.endswith(".hs"))]
prolog_files = [f for f in listdir(dir4) if isfile(join(dir4, f))]
python_files = [f for f in listdir(dir5) if isfile(join(dir5, f))]


html_file = 'C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\Overview.html'
f = open(html_file,'w')

message = """<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
		<title>Overview</title>
	</head>
		<body style = "background-color:powderblue;">
			<h1>CSC 344 Overview</h1>
			<h3>Assignment 1 : Programming Language C</h3>
				<ol>
					<li><a href=\"""" + dir1 + '\\{}'.format(c_files[0]) + """\">""" + c_files[0] + """</a></li>
					<li><a href=\"""" + dir1 + '\\{}'.format(c_files[1]) + """\">""" + c_files[1] + """</a></li>
					<li><a href=\"""" + dir1 + '\\{}'.format(c_files[2]) + """\">""" + c_files[2] + """</a></li>
					<li><a href=\"""" + dir1 + '\\{}'.format(c_files[3]) + """\">""" + c_files[3] + """</a></li>
				</ol>
			<h3>Assignment 2 : Programming Language Clojure</h3>
				<ol>
					<li><a href=\"""" + dir2 + '\\{}'.format(clojure_files[0]) + """\">""" + clojure_files[0] + """</a></li>
				</ol>
			<h3>Assignment 3 : Programming Language Haskell</h3>
				<ol>
					<li><a href=\"""" + dir3 + '\\{}'.format(haskell_files[0]) + """\">""" + haskell_files[0] + """</a></li>
				</ol>
			<h3>Assignment 4 : Programming Language Prolog</h3>
				<ol>
					<li><a href=\"""" + dir4 + '\\{}'.format(prolog_files[0]) + """\">""" + prolog_files[0] + """</a></li>
				</ol>
			<h3>Assignment 5 : Programming Language Python</h3>
				<ol>
					<li><a href=\"""" + dir5 + '\\{}'.format(python_files[0]) + """\">""" + python_files[0] + """</a></li>
				</ol>
			<h3>Symbols File</h3>
				<ol>
					<li><a href=\"""" + rootDir + '\\{}'.format(symbolsFileName) + """\">""" + symbolsFileName + """</a></li>
				</ol>
		</body>
</html>"""

f.write(message)
f.close()

#webbrowser.open_new_tab('C:\\Users\\XXXXXXXXXX\\Desktop\\csc344\\Overview.html')