#!/usr/bin/env python3

"""
csvmigrate.py
author: Nathan Taylor <nbtaylor@gmail.com>

csvmigrate consumes a csv file of data containing certain columns, and
adds them to the database.  The CSV must have the following columns:

    - "TYPE"
    - "GEO"
    - "Language"
    - "Concept"
    - "Original Term"
    - "Original Gloss"

    - "Bib-Source"
    - "Page number"

usage: csvmigrate.py <path_to_csv>.csv
"""

import csv
import os
import sys
import time

from collections import defaultdict

concepts = defaultdict(list)

def process_row(row):
    try:
        term = row["Original Term"]
        concept = row["Concept"]
        if term and concept:
            concepts[concept].append(term)
    except KeyError:
        pass

def main():
    b = time.time()
    with open(sys.argv[1], newline='', encoding='utf-8-sig') as f:
        rows = csv.DictReader(f, quotechar='"', dialect='excel')
        n = 0
        for row in rows:
            process_row(row)
            n += 1
    e = time.time()
    for concept in concepts:
        term = concepts[concept]
        print("{} = {}".format(concept, term))
    print("Processed {} entries in {:4.2f} seconds".format(n, (e-b)))


if __name__ == "__main__":
    main()
