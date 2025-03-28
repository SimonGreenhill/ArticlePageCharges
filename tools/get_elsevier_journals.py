#!/usr/bin/env python3
# coding=utf-8
"""..."""

import requests
from io import BytesIO

from openpyxl import load_workbook

# from https://www.elsevier.com/open-access

def read(filename):
    wb = load_workbook(filename = filename)
    header = ['ISSN', 'Title', 'Business model', 'USD', 'EUR', 'GBP', 'JPY']
    for i, row in enumerate(wb.worksheets[0].iter_rows()):
        if i > 3 and row[1].value is not None:
            d = dict(zip(header, [c.value for c in row]))
            d['URL'] = row[1].hyperlink.target
            yield d


def format_journal(j):
    if ',' in j:
        return '"%s"' % j
    else:
        return j



for o in read('elsevier-2025-03-28.xlsx'):
    # Date,Journal,Publisher,Cost,URL,Comment
    if o['USD'] == '**':
        # APC is waived (new journal), or sponsored by a third party, or invoiced directly to authors. 
        # ignore these for now
        continue
    print("2025-03-28,%s,Elsevier,%s,%s,%s" % (
        format_journal(o['Title']),
        "$%d" % o['USD'],
        o['URL'],
        o['Business model']
    ))

