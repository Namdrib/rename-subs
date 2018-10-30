# rename-subs
Command line program used to mass-rename subtitle files to match media files

## Requirements
- python3
	- argparse


## Usage
From running `python3 rename_subs/rename_subs.py -h` or `./reneame_subs/rename_subs.py`

```
usage: rename_subs.py [-h] [-d DIRECTORY] [-t] [-v]

Set up options for sub renaming
It is strongly recommended to use -tv on the first run to see what will be modified

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        target directory (default: current directory)
  -t, --test            do not run any commands
  -v, --verbose         verbose output
```
