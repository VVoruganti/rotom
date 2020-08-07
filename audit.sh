#!/bin/bash

# TODO add ability to clone git repo instead

# Check if live.txt and dead.txt are here and delete them if they exist
LIVE=live.txt
DEAD=dead.txt

if test -f "$LIVE"; then
    rm $LIVE
fi

if test -f "$DEAD"; then
    rm $DEAD
fi

# Store current directory and go to target directory
CUR=$(pwd)
cd $1

# Grep for links line by line
if command -v rg &> /dev/null; then # use ripgrep if it exists
    rg -e https?:\/\/\(www\.\)?[-a-zA-Z0-9@:%._\+~#=]\{1,256\}\.[a-zA-Z0-9\(\)]\{1,6\}\b\([-a-zA-Z0-9\(\)@:%_\+.~#?\&\/\/=]*\)[-a-zA-Z]\/? -o -N --no-filename > /tmp/link-audit.txt
else # or just use regular grep
    grep -e https?:\/\/\(www\.\)?[-a-zA-Z0-9@:%._\+~#=]\{1,256\}\.[a-zA-Z0-9\(\)]\{1,6\}\b\([-a-zA-Z0-9\(\)@:%_\+.~#?\&\/\/=]*\)[-a-zA-Z]\/? -o -N --no-filename > /tmp/link-audit.txt
fi
# Additional flags to check
# --no-ignore to disable respecting .gitignore TODO 

# Check links
while read link; do
    if curl -s --head "$link" | head -n 1 | grep " [23].." > /dev/null; then # use curl to check status
        echo "$link" >> $CUR/live.txt # if it's valid add to live.txt
    else
        echo "$link" >> $CUR/dead.txt # if dead add to dead.txt
    fi
done < /tmp/link-audit.txt

echo "These are the dead links\n"
cat $CUR/dead.txt

