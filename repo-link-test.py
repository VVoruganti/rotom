import re
import requests
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import NewConnectionError
from os.path import join, isfile, isdir, dirname, abspath
from os import listdir
from sys import argv
from subprocess import run
from enum import Enum
from colorama import Fore, Back, Style
# Make the regex for the URI
# Sourced this regex from https://ihateregex.io
#url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)')
url_match = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)[-a-zA-Z]\/?')

curdir = dirname(abspath(__file__))
# Get url of the repo to pull from 
# clone the input repo 
if(len(argv) > 1):
    repo = argv[1]
    if(isdir(join(curdir,"test-repo"))):
        run(args=["rm", "-rf", "test-repo"])
    run(args=["git", "clone", repo, "test-repo/"])
# TODO look into possible cloning it to the /tmp directory and cleaning it at the end 

matches = {} # A dictionary that shows all the links in each file every key is a file
links = {} # A dictionary that shows the status of each link every key is a link
# Main recrsive method that runs the searching on the repository
# will recursively check each file for matches to the regex and add them to 
# a global array of matches
# TODO Look into adding option to respect gitignore
def recursive_search(directory):
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
                        match = re.finditer(url_match, line)
                        if(match != None):
                            if(not file_path in matches):
                                matches[file_path] = []
                            for link in match:
                                matches[file_path].append([link.group(), False])
                                links[link.group()] = False
                    except UnicodeDecodeError:
                        print("    Following file has encoding issue{}".format(filename))
        else:
            recursive_search(file_path)

class ConnectionCodes(Enum):
    CONNECT = 1,
    TIMEOUT = 2,
    ERROR = 3

print("\n Now checking validity of each link, there are {} links \n".format(len(links)))
#https://realpython.com/python-requests/ - guideline for how to go about testing

def check_links():
    global links
    print("There are {} links to check".format(len(links)))
    tracker = 0
    for link in links:
        try:
            requests.get(link, timeout=3)
        except Timeout:
 #           print("{} ---- Time out".format(link))
            links[link] = ConnectionCodes.TIMEOUT
        except ConnectionError:
 #           print("{} ---- Connection Error".format(link))
            links[link] = ConnectionCodes.ERROR
        except Exception:
 #            print("\n")
 #            print(link)
 #            print(type(e))
 #            print(e.args)
 #            print(e)
 #            print("\n")
             links[link] = ConnectionCodes.ERROR
        else:
             links[link] = ConnectionCodes.CONNECT
 #             print("{} is valid".format(link))
        finally:
            tracker += 1
            if(tracker % 10 == 0):
                print("{} out of {}".format(tracker, len(links)))




def print_report():
    for file in matches:
        if(len(matches[file]) > 0):
            print(Style.RESET_ALL + "File: {}".format(file))
        for match in matches[file]:
            match[1] = links[match[0]]
            #links[match[0]] = match[1]
            if(match[1] == ConnectionCodes.CONNECT):
                print(Fore.GREEN + "    {match} ------ | STATUS : CONNECT".format(match=match[0]))
            elif(match[1] == ConnectionCodes.TIMEOUT):
                print(Fore.MAGENTA + "    {match} ------ | STATUS : TIMEOUT".format(match=match[0]))
            else:
                print(Fore.RED + "    {match} ------ | STATUS : ERROR".format(match=match[0]))

recursive_search(join(curdir,"test-repo"))

# broken into different functions to make debugging easier. Can easily turn off and of features
check_links()
print_report()
