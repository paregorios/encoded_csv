"""Intelligently read encoded CSV files.

This module provides a single function: get_csv(), which is used to read
an encoded CSV file.
"""

import chardet
import codecs
import csv
import io
from itertools import islice
import os


def get_csv(csv_file, skip_header_lines=0, encoding=''):
    """Read content from an encoded CSV file.

    We assume first row (after discarding any header lines) has column names.

    Arguments:

     * csv_file: path to CSV file to open
     * skip_header_lines: number of lines to discard in the assumption that
                          they constitute a file header of some sort
                          (default is to skip no lines)
     * encoding: text encoding used in file (default is to attempt best guess)

    Returns a tuple, in which the first item is a list of the field names. The
    second item is a list of ordered dictionaries, each containing the data
    read from a given line of the CSV file.
    """
    rpath = os.path.realpath(csv_file)

    # try to guess the encoding, if necessary
    if encoding == '':
        num_bytes = min(32, os.path.getsize(rpath))
        raw = open(rpath, 'rb').read(num_bytes)
        if raw.startswith(codecs.BOM_UTF8):
            e = 'utf-8-sig'
        else:
            e = chardet.detect(raw)['encoding']
    else:
        e = encoding

    # open the file and read into a list of dictionaries
    with io.open(rpath, 'r', encoding=e) as f:
        content = []
        reader = csv.DictReader(islice(f, skip_header_lines, None))
        for row in reader:
            content.append(row)
    field_names = list(content[0].keys())

    return (field_names, content)
