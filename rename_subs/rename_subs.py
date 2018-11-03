#!/usr/bin/env python3
"""
Created on 19 Feb. 2018

@author: Namdrib
"""
import argparse
import glob
import re
import subprocess


def filename_without_extension(filename):
    return filename[:filename.rfind('.')]


def get_extension(filename):
    return filename[filename.rfind('.'):]


# Given an input scene release name, extract the part of it
# that uniquely identifies the release
# for movies: movie.name.year
# for tv shows: tv.show.name.sxxexx
# up to year, but not the resolution. accounts for movies like
# "2012.2009.1080p"
movie_id_regex = "^.*(\.|\ )([1|2]\d{3})(?!p)"
# up to season/episode, allow fused episodes (e.g. s01e01e02)
tvshow_id_regex = "^.*(\.|\ )s\d{2}((e\d{2})+)"
together = "({})|({})".format(tvshow_id_regex, movie_id_regex)
id_regex = re.compile(together)


def get_filename_identifier(filename):
    return id_regex.match(filename.lower())


def video_file_extensions():
    return ['avi', 'm4a', 'mkv', 'mp4', 'mpeg', 'mpg', 'webm']


def sub_file_extensions():
    return ['ass', 'smi', 'srt', 'ssa', 'sub', 'txt', 'usf']


def get_files_with_extension(directory, extensions):
    """
    extensions should be a list
    """
    files = []
    for extension in extensions:
            # files += glob.glob("*.{}".format( extension))
        files += glob.glob("{}/*.{}".format(directory, extension))
    return files


def rename_subs(directory='.', test=False, verbose=False):
    """
    for each video file without a corresponding subtitle file
        if there is a subtitle file with incorrect naming
            copy the video file's name (w/o extension) to sub name
    """

    for video_name in get_files_with_extension(directory, video_file_extensions()):
        no_extension = filename_without_extension(video_name)
        identifier = get_filename_identifier(no_extension)

        do_rename = False
        reason = '' # reason for not renaming

        # Find the corresponding subtitle file
        for sub_name in get_files_with_extension(directory, sub_file_extensions()):
            # if identifier.group().lower() in sub_name.lower():
            # if string.replace(identifier.group().lower(), " ", ".") in
            # string.replace(sub_name.lower(), " ", "."):
            if identifier.group().lower().translate(str.maketrans(' ', '.')) in sub_name.lower().translate(str.maketrans(' ', '.')):
                new_sub_name = no_extension + get_extension(sub_name)
                if sub_name == new_sub_name:
                    reason = 'sub already correctly named'
                    break
                if verbose:
                    print("Match for {}".format(video_name))
                    print("{} -> {}".format(sub_name, new_sub_name))
                if test:
                    reason = 'test run'
                else:
                    subprocess.run(["mv", sub_name, new_sub_name])
                    do_rename = True
                    break

        if verbose:
            if not do_rename:
                print("skipping {}, reason: {}".format(video_name, reason))
            print()


def argparse_setup():
    """
    Setting up the optional command line arguments
    Called in main only
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Set up options for sub renaming\nIt is strongly recommended to use -tv on the first run to see what will be modified'
    )

    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='target directory (default: current directory)'
    )

    parser.add_argument(
        '-t', '--test',
        default=False,
        action='store_true',
        help='do not run any commands'
    )

    parser.add_argument(
        '-v', '--verbose',
        default=False,
        action='store_true',
        help='verbose output'
    )

    return parser


def main():
    parser = argparse_setup()
    args = parser.parse_args()

    # Maybe take more args for more complicated uses
    rename_subs(directory=args.directory,
                test=args.test, verbose=args.verbose)


if __name__ == '__main__':
    main()
