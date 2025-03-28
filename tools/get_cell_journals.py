#!/usr/bin/env python3
# coding=utf-8
"""..."""

import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

URL = "https://www.cell.com/open-access"

is_euro_amount = re.compile(r"""(£\d+,\d+)""")

def get_cost(text):
    m = is_euro_amount.findall(text)
    if len(m):
        return m[0].replace(",", "")
    else:
        print("ERROR PARSING COST FROM:")
        print(text)
        return None

driver = webdriver.Firefox()
driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

table = soup.find(id="pricingTbl")

header = [x.text for x in table.find_all('th')]

for row in table.find_all("tr"):
    cells = dict(zip(header, [c.text for c in row.find_all('td')]))
    if not len(cells):  # empty row
        continue
    if cells['Journal'] in ('Full open access', 'Hybrid open access'):
        continue

    try:
        cost_text = cells['Open access fee (GBP, EURO, USD)(excluding taxes)']
    except KeyError:
        print("Failure parsing:")
        print(row.find_all('td'))
        raise
    
    
    cost = get_cost(cost_text)
    
    print("2024-01-14,%s,%s,%s,'%s',Cell Press" % (
        cells['Journal'],
        cost,
        URL,
        cost_text.replace("'", '"')  # should use csv writer
    ))

