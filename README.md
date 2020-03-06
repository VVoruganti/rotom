# Git Repository URL Tester

This project is being made in response to the fact that many old projects contain dead links
this tool will make it easy to quickly check all of the links in a repository to 
find the location of any/all links and determine if they are dead or not. 

## Usage

With the repo cloned you can use the `repo-link-tester.py` to test any repo you would like. Simply
run the application and pass in the link to the repo of your choice as an argument in the command line

```bash
python repo-link-tester.py https://www.github.com/user/repo
```
this will clone the repo and run the analysis

## Development

This project was developed using python 3.7.4

1. clone the repo
2. Setup a virtual environment and download dependencies
   
```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements
```
3. Make changes as needed

## TODO

- [ ] Add a flag to make it possible to point to an existing repo on a end system 

## Changelog


