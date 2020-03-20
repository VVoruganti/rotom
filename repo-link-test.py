import re
import requests
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import NewConnectionError
from os.path import join, isfile, isdir, dirname, abspath
from os import listdir
from sys import argv
from subprocess import run
from enum import Enum
# Make the regex for the URI
# Sourced this regex from https://ihateregex.io
#url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)')
url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)[-a-zA-Z\/]')

curdir = dirname(abspath(__file__))
# Get url of the repo to pull from 
# clone the input repo 
if(len(argv) > 1):
    repo = argv[1]
    if(isdir(join(curdir,"test-repo"))):
        run(args=["rf", "-rf", "test-repo"])
    run(args=["git", "clone", repo, "test-repo/"])
# TODO look into possible cloning it to the /tmp directory and cleaning it at the end 

matches = {}
links = {}
# Main recrsive method that runs the searching on the repository
# will recursively check each file for matches to the regex and add them to 
# a global array of matches
def recursive_search(directory):
    # print(directory)
    global url_match
    global matches
    global links
    files = listdir(directory)
    print(files)
    for filename in files:
        print("    Checking following file {}".format(filename))
        file_path = join(directory, filename)
        if(isfile(file_path)):
            with open(file_path, "r", encoding="latin-1") as file:
                for line in file:
                    try:
                        # TODO check if multiple links on the same line
                        match = re.search(url_match, line)
                        if(match != None):
                            if(not file_path in matches):
                                matches[file_path] = []
                            matches[file_path].append([match, False])
                            links[match.group()] = False
                    except UnicodeDecodeError:
                        print("    Following file has encoding issue{}".format(filename))
        else:
            recursive_search(file_path)

class ConnectionCodes(Enum):
    CONNECT = 1,
    TIMEOUT = 2,
    ERROR = 3

#recursive_search(join(curdir,"temp"))
#print(matches)
#print(len(matches))

print("\n Now checking validity of each link, there are {} links \n".format(len(links)))
#https://realpython.com/python-requests/ - guideline for how to go about testing

def check_links():
    global links
    for link in links:
        try:
            r = requests.get(link, timeout=3)
        except Timeout:
            print("{} ---- Time out".format(link))
            links[link] = ConnectionCodes.TIMEOUT
        except ConnectionError:
            print("{} ---- Connection Error".format(link))
            links[link] = ConnectionCodes.ERROR
        except Exception as e:
             print("\n")
             print(link)
             print(type(e))
             print(e.args)
             print(e)
             print("\n")
             links[link] = ConnectionCodes.ERROR
        else:
             links[link] = ConnectionCodes.CONNECT
             print("{} is valid".format(link))

def print_report():
    for file in matches:
        print("File: {}".format(file))
        for match in matches[file]:
            match[1] = links[match[0].group()]
            #links[match[0]] = match[1]
            if(match[1] != ConnectionCodes.CONNECT):
                print("    {match} ------ | STATUS : {status}".format(match=match[0].group(), status=match[1]))

recursive_search(join(curdir,"test-repo"))

# broken into different functions to make debugging easier. Can easily turn off and of features
check_links()
print_report()
# TODO have a final output that looks similar to how rip grep organizes its output sampel command below
# rg -e https:\/\/
