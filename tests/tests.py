"""Tests for the encoded_csv package."""

__author__ = 'Tom Elliott'
__copyright__ = 'Copyright ©️ 2017 New York University'
__license__ = 'See LICENSE.txt'
__version__ = '0.1'

from airtight.logging import flog
import csv
from inspect import getsourcefile
from nose.tools import assert_equal, assert_not_equal, raises
from encoded_csv import get_csv
from os.path import dirname, join as joinpath, realpath
import unittest


class _ExcelMutant(csv.excel):
    def __init__(self, **kwargs):
        super(_ExcelMutant, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)


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

    def _load(self, **kwargs):
        kwargs['csv_file'] = joinpath(self.data_dir, kwargs['csv_file'])
        return get_csv(**kwargs)

    def _execute(self, **kwargs):
        d = self._load(**kwargs)
        assert_equal(self.length, len(d['content']))
        assert_equal(self.fields, d['fieldnames'])
        row = d['content'][2]
        assert_equal('3', row['pet_id'])
        assert_equal('cat', row['species'])
        assert_equal('Garfunkle', row['name'])
        assert_equal('The Great Orange One', row['nicknames'])
        assert_equal(3, len(row['behaviors'].split(',')))
        assert_equal(
            'friendly, talkative, not fit for indoor life',
            row['behaviors'])
        assert_equal('8', row['weight'])
        return d

    def _compare_dialects(self, target, candidate):
        for a in [a for a in dir(target) if a[0] != '_' and a != 'strict']:
            flog(a)
            attr_t = getattr(target, a)
            attr_c = getattr(candidate, a)
            tt = type(attr_t)
            tc = type(attr_c)
            if tt == int and tc == bool:
                attr_c = int(attr_c)
            elif tt != tc:
                raise Exception(
                    'Type mismatch for "{}". Target is {}, but candidate is '
                    '{}.'.format(a, tt, tc))
            else:
                assert_equal(getattr(target, a), getattr(candidate, a))

    def test_excel(self):
        kwargs = {'csv_file': 'pets_excel.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('ascii', d['encoding'])
        row = d['content'][4]
        assert_equal('_____', row['name'])  # clobbered on export from excel

    def test_excel_msdos(self):
        kwargs = {'csv_file': 'pets_excel_msdos.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('ascii', d['encoding'])
        row = d['content'][4]
        assert_equal('_____', row['name'])  # clobbered on export from excel

    def test_excel_tabs(self):
        kwargs = {'csv_file': 'pets_excel_tabs.txt'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel-tab'), d['dialect'])
        assert_equal('ascii', d['encoding'])
        row = d['content'][4]
        assert_equal('_____', row['name'])  # clobbered on export from excel

    def test_excel_utf8(self):
        kwargs = {'csv_file': 'pets_excel_utf8.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('utf-8-sig', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_excel_windows(self):
        kwargs = {'csv_file': 'pets_excel_windows.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('ascii', d['encoding'])
        row = d['content'][4]
        assert_equal('_____', row['name'])  # clobbered on export from excel

    def test_libre_utf8_comma_dquote(self):
        kwargs = {'csv_file': 'pets_libre_utf8_comma_dquote.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('utf-8', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_libre_utf8_comma_dquoteall(self):
        kwargs = {'csv_file': 'pets_libre_utf8_comma_dquoteall.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('utf-8', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_libre_utf8_comma_squote(self):
        kwargs = {'csv_file': 'pets_libre_utf8_comma_squote.csv'}
        d = self._execute(**kwargs)
        target_dialect = _ExcelMutant(quotechar="'", doublequote=False)
        self._compare_dialects(target_dialect, d['dialect'])
        assert_equal('utf-8', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_libre_utf16_comma_dquote(self):
        kwargs = {'csv_file': 'pets_libre_utf16_comma_dquote.csv'}
        d = self._execute(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])
        assert_equal('UTF-16', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_libre_utf8_colon_dquote(self):
        kwargs = {'csv_file': 'pets_libre_utf8_colon_dquote.csv'}
        d = self._execute(**kwargs)
        target_dialect = _ExcelMutant(delimiter=':', doublequote=False)
        self._compare_dialects(target_dialect, d['dialect'])
        assert_equal('utf-8', d['encoding'])
        row = d['content'][4]
        assert_equal('Ἀθηνᾶ', row['name'])

    def test_hgc_prologue(self):
        kwargs = {
            'csv_file': 'HGC-Populated-Places.csv',
            'skip_lines': 6
        }
        d = self._load(**kwargs)
        self._compare_dialects(csv.get_dialect('excel'), d['dialect'])

