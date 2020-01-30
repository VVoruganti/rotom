import re
import http
from sys import argv
# Make the regex for the URI
url_match = re.compile("")

# Get url of the repo to pull from 
repo = argv[1]


