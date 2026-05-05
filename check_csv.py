#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2025 Simon J. Greenhill'
__license__ = 'New-style BSD'

import csv

PUBLISHERS = [
    '',
    'AAAS',
    'Cambridge University Press',
    'Cell Press',
    'Elsevier',
    'MIT Press',
    'National Academy of Science',
    'Oxford University Press',
    'Royal Society',
    'Springer Nature',
    'De Gruyter',
]

KNOWN_MISSING_URLS = [
    'Environmental Toxicology and Chemistry',
    'Integrated Environmental Assessment and Management',
    'Journal of American History',
    
]

def get(filename):  # csv only
    with open(filename, mode='r') as handle:
        for row in csv.DictReader(handle):
            yield row


def is_cost(value):
    value = value.replace("$", "").replace("£", "").replace("¥", "").replace("€", "")
    try:
        float(value)
    except:
        return False
    return True


if __name__ == '__main__':
    errors = 0
    for i, o in enumerate(get('charges.csv'), 0):
        if o['Journal'] not in KNOWN_MISSING_URLS and not o['URL'].startswith('htt'):
            print("error - URL", i, o)
            errors += 1
            
        if o['Publisher'] not in PUBLISHERS:
            print("error - publisher", i, o)
            errors += 1

        if o['Cost'] is None:
            print("error - costA", i, o)
            errors += 1
        
        if is_cost(o['Cost']) == False:
            print("error - costB", i, o)
            errors += 1
            

        if o['Comment'] is None:
            print("error - comment", i, o)
            errors += 1

        
    print(errors)