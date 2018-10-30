# rename-subs
Command line program used to mass-rename subtitle files to match media files

## Requirements
- python3
	- argparse


## Usage
From running `python3 rename_subs.py -h`

```
usage: rename_subs.py [-h] [-d DIRECTORY] [-t] [-v] [-i] [-c]

Set up options for sub renaming
It is strongly recommended to use -tv on the first run to see what will be modified

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        target directory (default: current directory)
  -t, --test            do not run any commands
  -v, --verbose         verbose output

test group:
  used for verifying functionality. does not edit existing files
  this functionality should be deprecated by unit testing ASAP

  -i, --init            initialise test files
  -c, --clean           clean files created using the -i flag and
                        corresponding transformations
```
