#!/usr/bin/env python3
# coding=utf-8
"""..."""

import requests
from io import BytesIO

from openpyxl import load_workbook

def read(filename):
    wb = load_workbook(filename = filename)
    header = None
    for i, row in enumerate(wb.worksheets[0].iter_rows()):
        if i == 3:
            header = [c.value for c in row]
        elif i > 3:
            yield dict(zip(header, [c.value for c in row]))
            #d['URL'] = row[1].hyperlink.target

#SPECIAL = {
#    '1000 Euro full-lenght (for society members 800 Euro), 800 Euro Scientific Note (for society members 600 Euro)': 
#}

def format_price(p):
    if p is None:
        return "€0", ""
    if len(p) == 0:
        return "€0", ""
    if p == 'none':
        return "€0", ""
    try:
        return "€%d" % int(p), ""
    except:
        raise ValueError("?? %s" % p)


special_cases = []
for o in read('DeGruyter_Journal_Price_List_2025__EUR__2024-11-10.xlsx'):
    # Date,Journal,Publisher,Cost,URL,Comment
    try:
        price, comment = format_price(o['APC EUR'])
    except Exception as e:
        #print('ERROR', e)
        special_cases.append(o)
        pass
    print("2025-31-03,%s,De Gruyter,%s,%s,%s" % (
        o['Title'].strip(),
        price,
        o['URL'],
        comment
    ))

print("============")
for o in special_cases:
    print("2025-31-03,%s,De Gruyter,%s,%s,%s" % (
        o['Title'].strip(),
        "?????",
        o['URL'],
        o['APC EUR']
    ))

    