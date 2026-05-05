#!/usr/bin/env python3
# coding=utf-8
"""..."""
import csv
import re
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://www.cell.com/open-access"

# Matches the first USD price in the cell, e.g. "$8,900" or "$7000"
first_price = re.compile(r'\$[\d,]+')

def get_cost(text):
    m = first_price.search(text)
    if m:
        return m.group(0).replace(",", "")
    print(f"ERROR PARSING COST FROM: {text!r}", file=sys.stderr)
    return None

def get_comment(text, cost):
    """Return any text after the leading price as a comment."""
    if cost and text.startswith(cost):
        return text[len(cost):].strip()
    return text

driver = webdriver.Firefox()
driver.get(URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

table = soup.find(id='pricingTbl')
headers = [th.get_text(strip=True) for th in table.find_all('th')]
cost_col = 'Open access fee(excluding taxes)'

writer = csv.writer(sys.stdout)
writer.writerow(['Date', 'Journal', 'Publisher', 'Cost', 'URL', 'Comment'])

for row in table.find_all('tr'):
    cells = dict(zip(headers, [td.get_text(strip=True) for td in row.find_all('td')]))
    if not cells:
        continue
    journal = cells.get('Journal', '').strip()
    if journal in ('Full open access', 'Hybrid open access', ''):
        continue

    cost_text = cells.get(cost_col, '')
    cost = get_cost(cost_text)
    comment = get_comment(cost_text, cost)

    writer.writerow([
        '2026-05-06',
        journal,
        'Cell Press',
        cost,
        URL,
        comment,
    ])
