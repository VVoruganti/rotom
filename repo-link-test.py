import re
import http
from os.path import join
from os import getcwd, listdir
from sys import argv
from subprocess import run
# Make the regex for the URI
url_match = re.compile("https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)")

# Get url of the repo to pull from 
repo = argv[1]

# clone the input repo 
run(args=["git", "clone", repo, "repo/"])

files = listdir("repo")

print(files)

matches = []
