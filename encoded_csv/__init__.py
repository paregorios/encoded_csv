"""Intelligently read encoded CSV files.

This module provides a single function: get_csv(), which is used to read
an encoded CSV file.
"""

from airtight.logging import flog
import chardet
import codecs
import csv
import io
from itertools import islice
import os


def get_csv(
    csv_file,
    skip_lines=0,
    encoding='',
    dialect='',
    fieldnames=[],
    sample_lines=100
):
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

    reader_kwargs = {}

    # encoding detection
    if encoding == '':
        num_bytes = min(1024, os.path.getsize(rpath))
        raw = open(rpath, 'rb').read(num_bytes)
        if raw.startswith(codecs.BOM_UTF8):
            file_encoding = 'utf-8-sig'
        else:
            file_encoding = chardet.detect(raw)['encoding']
    else:
        file_encoding = encoding

    # force fieldnames if necessary
    if len(fieldnames) != 0:
        reader_kwargs['fieldnames'] = fieldnames

    with io.open(rpath, 'r', encoding=file_encoding) as f:

        # dialect detection
        if dialect == '':
            for _ in range(skip_lines):
                next(f)
            sample = []
            for _ in range(sample_lines):
                sample.append(f.readline())
            sample = ''.join(sample)
            sniffer = csv.Sniffer()
            reader_kwargs['dialect'] = sniffer.sniff(sample)
        else:
            reader_kwargs['dialect'] = dialect

        # read into a list of dictionaries
        f.seek(0)
        content = []
        reader = csv.DictReader(islice(f, skip_lines, None), **reader_kwargs)
        for row in reader:
            content.append(row)

    if len(content) > 0:
        return (
            {
                'content': content,
                'fieldnames': list(content[0].keys()),
                'encoding': file_encoding,
                'dialect': reader_kwargs['dialect']
            })
    else:
        return None
