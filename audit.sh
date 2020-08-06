#!/bin/bash

# Grep for links line by line
rg -e https?:\/\/\(www\.\)?[-a-zA-Z0-9@:%._\+~#=]\{1,256\}\.[a-zA-Z0-9\(\)]\{1,6\}\b\([-a-zA-Z0-9\(\)@:%_\+.~#?\&\/\/=]*\)[-a-zA-Z]\/? -o -N > /tmp/link-audit.txt
# Additional flags to check
# --no-ignore to disable respecting .gitignore

# Check links
while read link; do
if host "$link" > /dev/null; then
# If host is live, print it into "live.txt" 
echo "$link" >> live.txt
fi
done < /tmp/link-audit.txt
