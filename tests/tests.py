"""Tests for the encoded_csv package."""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.1'

from nose.tools import assert_equal, assert_not_equal, raises
from encoded_csv import get_csv
import unittest


class SpaceTests(unittest.TestCase):

    def setUp(self):
        self.data_dir = 'The quick brown fox jumped over the lazy sea urchin.'

    def tearDown(self):
        pass

    def test_empty(self):
        pass
