"""Intelligently read encoded CSV files."""

import chardet
import codecs
import csv
import io
from itertools import islice
import os


def get_csv(csv_file, skip_header_lines=0, encoding=''):
    rpath = os.path.realpath(csv_file)

    # try to guess the encoding
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
