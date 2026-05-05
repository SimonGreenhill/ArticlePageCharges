#!/usr/bin/env python3
# coding=utf-8
"""..."""
import csv
import re
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.cell.com/open-access"

is_euro_amount = re.compile(r"""(£\d+,\d+)""")

def get_cost(text):
    m = is_euro_amount.findall(text)
    if len(m):
        return m[0].replace(",", "")
    else:
        print("ERROR PARSING COST FROM:", file=sys.stderr)
        print(text, file=sys.stderr)
        return None

driver = webdriver.Firefox()
driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

table = soup.find(id="pricingTbl")

header = [x.text for x in table.find_all('th')]

writer = csv.writer(sys.stdout)
writer.writerow(['Date', 'Journal', 'Publisher', 'Cost', 'URL', 'Comment'])

for row in table.find_all("tr"):
    cells = dict(zip(header, [c.text for c in row.find_all('td')]))
    if not len(cells):  # empty row
        continue
    if cells['Journal'] in ('Full open access', 'Hybrid open access'):
        continue

    try:
        cost_text = cells['Open access fee (GBP, EURO, USD)(excluding taxes)']
    except KeyError:
        print("Failure parsing:", file=sys.stderr)
        print(row.find_all('td'), file=sys.stderr)
        raise

    cost = get_cost(cost_text)
    writer.writerow([
        '2024-01-14',
        cells['Journal'],
        'Cell Press',
        cost,
        URL,
        cost_text,
    ])
