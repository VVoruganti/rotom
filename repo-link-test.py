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

# TODO change to a dictionary that will map a filepath to the links in it. Will help with final output
matches = []

# Main recrsive method that runs the searching on the repository
# will recursively check each file for matches to the regex and add them to 
# a global array of matches
def recursive_search(directory):
    # print(directory)
    global url_match
    global matches
    files = listdir(directory)
    # print(files)
    for filename in files:
        # print("    Checking following file {}".format(filename))
        file_path = join(directory, filename)
        if(isfile(file_path)):
            with open(file_path, "r", encoding="latin-1") as file:
                try:
                    text = " ".join(file.readlines())
                    match = re.search(url_match,text)
                    if(match != None):
                        # print(match)
                        matches.append((file_path, match))
                except UnicodeDecodeError as e:
                    print("     Following file has encoding issue {}".format(filename))
        else:
            recursive_search(file_path)

recursive_search(join(curdir,"test-repo"))
#print(matches)
#print(len(matches))

for match in matches:
    print("{} --- in file -- {}".format(match[1].group(), match[0]))

# TODO have a final output that looks similar to how rip grep organizes its output sampel command below
# rg -e https:\/\/
