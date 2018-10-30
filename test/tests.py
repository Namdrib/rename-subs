"""
Created on 30 Oct. 2018

@author: Namdrib
"""
import os
import subprocess
import unittest

import rename_subs


class TestRenameSubs(unittest.TestCase):

    def setUp(self):
        self.test_media = [
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

        self.test_subs = [
            'test.tv.show.name.s01e01e02.srt',
            'test.tv.show.name.s01e03.srt',
            'test.tv.show.name.s01e04.1080p.srt',
            'test.tv.show.name.s01e05.1080p.srt',
            'Title.of.the.Movie.2000.Source.Codec-GROUP.srt',
            'Movie.With.Resolution.1080.BDRIP.more.unecessary.things.srt',
            'test.tv.show.S02E01.1080p.WEB-DL.DD5.1.H264.srt',
            'test tv show S02E02 1080p WEB-DL DD5-1 H264.srt',
        ]

        self.expected = [
            'test.tv.show.name.s01e01e02.episode.name.srt',
            'test.tv.show.name.s01e03.episode.name.srt',
            'test.tv.show.name.s01e04.Episode.Name.WEB-DL.srt',
            'test.tv.show.name.s01e05.1080p.srt',
            'Title.Of.The.Movie.2000.source.codec-group.srt',
            'Movie.With.Resolution.1080.1080p.things.srt',
            'test tv show S02E01 episode name.srt',
            'test.tv.show.S02E02.episode.name.srt',
        ]

        self.directory = 'test_dir'

        # Create the test media and sub files
        if not os.path.exists(self.directory):
            subprocess.run(['mkdir', self.directory])
        # Create test media files
        for test_media in self.test_media:
            subprocess.run(['touch', test_media], cwd=self.directory)

        # Create test subtitle files
        for test_sub in self.test_subs:
            subprocess.run(['touch', test_sub], cwd=self.directory)

    def tearDown(self):
        """
        remove the created test directory
        """
        subprocess.run(['rm', '-r', self.directory])

    def test_rename_subs(self):
        rename_subs.rename_subs(self.directory, False, False)

        for item in self.test_media:
            item = self.directory + '/' + item
            self.assertTrue(os.path.isfile(item), item)
        for item in self.expected:
            item = self.directory + '/' + item
            self.assertTrue(os.path.isfile(item), item)
