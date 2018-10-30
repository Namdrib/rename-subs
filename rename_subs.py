#!/usr/bin/env python3
"""
Created on 19 Feb. 2018

@author: Namdrib
"""
import argparse
import glob
import os
import re
import subprocess

test_videos = [
    'test.tv.show.name.s01e01e02.episode.name.mkv',
    'test.tv.show.name.s01e03.episode.name.m4a',
    'test.tv.show.name.s01e04.Episode.Name.WEB-DL.m4a',
    'test.tv.show.name.s01e05.1080p.m4a',
    'Title.Of.The.Movie.2000.source.codec-group.mkv',
    'Movie.With.Resolution.1080.1080p.things.mkv',
    'file.without.corresponding.sub.2017.mkv',
    'test tv show S02E01 episode name.mkv',
    'test.tv.show.S02E02.episode.name.mkv',
]

test_subs = [
    'test.tv.show.name.s01e01e02.srt',
    'test.tv.show.name.s01e03.srt',
    'test.tv.show.name.s01e04.1080p.srt',
    'test.tv.show.name.s01e05.1080p.srt',
    'Title.of.the.Movie.2000.Source.Codec-GROUP.srt',
    'Movie.With.Resolution.1080.BDRIP.more.unecessary.things.srt',
    'test.tv.show.S02E01.1080p.WEB-DL.DD5.1.H264.srt',
    'test tv show S02E02 1080p WEB-DL DD5-1 H264.srt',
]


def filename_without_extension(input):
    return input[:input.rfind('.')]


def get_extension(input):
    return input[input.rfind('.'):]


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


def get_filename_identifier(input):
    return id_regex.match(input.lower())


def initialise_files(directory='.', test=False, verbose=False):
    """
    Create two fake video files and corresponding subtitle files
    """

    if not os.path.exists(directory):
        subprocess.run(['mkdir', directory])
    # Create test video files
    for test_video in test_videos:
        if verbose:
            print("Create {}".format(directory + '/' + test_video))
        if not test:
            subprocess.run(['touch', test_video], cwd=directory)

    # Create test subtitle files
    for test_sub in test_subs:
        if verbose:
            print("Create {}".format(directory + '/' + test_sub))
        if not test:
            subprocess.run(['touch', test_sub], cwd=directory)


def clean(directory='.', test=False, verbose=False):
    # Delete existing test video files
    for test_video in [x for x in test_videos if os.path.isfile(x)]:
        if verbose:
            print("Delete {}".format(directory + '/' + test_video))
        if not test:
            subprocess.run(['rm', test_video], cwd=directory)

        # Check for transformed sub, delete if exists
        transformed_sub = filename_without_extension(test_video) + ".srt"
        if os.path.isfile(transformed_sub):
            if verbose:
                print("Delete {}".format(directory + '/' + transformed_sub))
            if not test:
                subprocess.run(['rm', transformed_sub], cwd=directory)

    # Delete existing test subtitle files
    for test_sub in [x for x in test_subs if os.path.isfile(x)]:
        if verbose:
            print("Delete {}".format(directory + '/' + test_sub))
        if not test:
            subprocess.run(['rm', test_sub], cwd=directory)


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
        # Find the corresponding subtitle file
        for sub_name in get_files_with_extension(directory, sub_file_extensions()):
            # if identifier.group().lower() in sub_name.lower():
            # if string.replace(identifier.group().lower(), " ", ".") in
            # string.replace(sub_name.lower(), " ", "."):
            if identifier.group().lower().translate(str.maketrans(' ', '.')) in sub_name.lower().translate(str.maketrans(' ', '.')):
                new_sub_name = no_extension + get_extension(sub_name)
                if verbose:
                    print("Match for {}".format(video_name))
                    print("{} -> {}".format(sub_name, new_sub_name))
                if not test:
                    subprocess.run(["mv", sub_name, new_sub_name])
                    do_rename = True
                    break

        if verbose:
            if not do_rename:
                print("skipping {}".format(video_name))
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

    test_group = parser.add_argument_group(
        'test group', 'used for verifying functionality. does not edit existing files\nthis functionality should be deprecated by unit testing ASAP')

    test_group.add_argument(
        '-i', '--init',
        default=False,
        action='store_true',
        help='initialise test files'
    )
    test_group.add_argument(
        '-c', '--clean',
        default=False,
        action='store_true',
        help='clean files created using the -i flag and corresponding transformations'
    )

    return parser


def main():
    parser = argparse_setup()
    args = parser.parse_args()

    if args.clean == True:
        clean(directory=args.directory, test=args.test, verbose=args.verbose)

    if args.init == True:
        initialise_files(directory=args.directory,
                         test=args.test, verbose=args.verbose)
    else:
        # Maybe take more args for more complicated uses
        rename_subs(directory=args.directory,
                    test=args.test, verbose=args.verbose)


if __name__ == '__main__':
    main()
