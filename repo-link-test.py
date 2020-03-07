import re
import requests
from requests.exceptions import Timeout
from os.path import join, isfile, isdir, dirname, abspath
from os import listdir
from sys import argv
from subprocess import run
# Make the regex for the URI
# Sourced this regex from https://ihateregex.io
#url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)')
url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)[-a-zA-Z\/]')

# TODO Figure out how to resolve below error
# Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7ff09409ee10>: Failed to establish
# a new connection: [Errno 101] Network is unreachable')


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
    print(files)
    for filename in files:
        print("    Checking following file {}".format(filename))
        file_path = join(directory, filename)
        if(isfile(file_path)):
            with open(file_path, "r", encoding="latin-1") as file:
                try:
                    text = " ".join(file.readlines())
                    match = re.search(url_match,text)
                    if(match != None):
                        # print(match)
                        matches.append((file_path, match, False))
                except UnicodeDecodeError as e:
                    print("     Following file has encoding issue {}".format(filename))
        else:
            recursive_search(file_path)

recursive_search(join(curdir,"test-repo"))
#print(matches)
#print(len(matches))

print("\n Now checking validity of each link \n")

# https://realpython.com/python-requests/ - guideline for how to go about testing
for match in matches:
    try:
        r = requests.get(match[1].group(), timeout=1)
    except Timeout:
        print("{} Timed out".format(match[1].group()))
    if (r.status_code != 200): 
        print("{} {}".format(match[1].group(), r.status_code))

# TODO have a final output that looks similar to how rip grep organizes its output sampel command below
# rg -e https:\/\/
