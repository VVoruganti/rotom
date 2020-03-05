import re
import http
from os.path import join, isfile, isdir, dirname, abspath
from os import listdir
from sys import argv
from subprocess import run
# Make the regex for the URI
# Sourced this regex from https://ihateregex.io
url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)')

curdir = dirname(abspath(__file__))
# Get url of the repo to pull from 
# clone the input repo 
if(len(argv) > 1):
    repo = argv[1]
    if(isdir(join(curdir,"test-repo"))):
        run(args=["rf", "-rf", "test-repo"])
    run(args=["git", "clone", repo, "test-repo/"])
# TODO look into possible cloning it to the /tmp directory and cleaning it at the end 

#files = listdir("test-repo")
#print(files)
#print(len(files))
matches = []

# for filename in files:
#     file_path = join(curdir, "test-repo", filename)
#     if(isfile(file_path)): # Check to make sure it is not a directory
#         file = open(file_path, "r")
#         text = " ".join(file.readlines())
#         match = re.search(url_match,text)
#         if(match != None):
#             print(match)
#     else:
#         recursive_search(filename)
#         print("test")
        # need a recursive step here

def recursive_search(directory):
    global url_match
    global matches
    files = listdir(directory)
    print(files)
    for filename in files:
        file_path = join(directory, filename)
        if(isfile(file_path)):
            with open(file_path, "r") as file:
                text = " ".join(file.readlines())
                match = re.search(url_match,text)
                if(match != None):
                    print(match)
                    matches.append(match)
        else:
            recursive_search(file_path)

recursive_search(join(curdir,"test-repo"))
# have a final output that looks similar to how rip grep organizes its output sampel command below
# rg -e https:\/\/
