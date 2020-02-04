import re
import http
from os.path import join, isfile
from os import getcwd, listdir
from sys import argv
from subprocess import run
# Make the regex for the URI
url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)')

# Get url of the repo to pull from 
# clone the input repo 
if(len(argv) > 1):
    repo = argv[1]
    run(args=["rf", "-rf", "repo"])
    run(args=["git", "clone", repo, "repo/"])
    
files = listdir("repo")
print(files)

matches = []

for filename in files:
    file_path = join("repo", filename)
    if(isfile(file_path)): # Check to make sure it is not a directory
        file = open(file_path, "r")
        text = " ".join(file.readlines())
        match = re.search(url_match,text)
        if(match != None):
            print(match)
    else:
        print("test")
        # need a recursive step here

def recursive_search(files):
    print(files)

