"""Tests for the encoded_csv package."""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.1'

from inspect import getsourcefile
from nose.tools import assert_equal, assert_not_equal, raises
from encoded_csv import get_csv
from os.path import dirname, join as joinpath, realpath
import unittest


class CSVTests(unittest.TestCase):

    def setUp(self):
        self.data_dir = joinpath(
            dirname(realpath(getsourcefile(lambda: 0))), 'data')
        self.fields = [
            'pet_id',
            'species',
            'name',
            'nicknames',
            'behaviors',
            'weight'
        ]
        self.length = 5

    def tearDown(self):
        pass

    def _execute(self, **kwargs):
        kwargs['csv_file'] = joinpath(self.data_dir, kwargs['csv_file'])
        fields, data = get_csv(**kwargs)
        assert_equal(self.length, len(data))
        assert_equal(self.fields, fields)

    def test_excel(self):
        kwargs = {'csv_file': 'pets_excel.csv'}
        self._execute(**kwargs)

    def test_excel_msdos(self):
        kwargs = {'csv_file': 'pets_excel_msdos.csv'}
        self._execute(**kwargs)

    def test_excel_tabs(self):
        kwargs = {'csv_file': 'pets_excel_tabs.txt'}
        self._execute(**kwargs)

