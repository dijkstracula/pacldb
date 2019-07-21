#!/usr/bin/env python3

"""
geounique.py
author: Nathan Taylor <nbtaylor@gmail.com>

csvmigrate consumes a csv file of data containing certain columns, and
confirms that every language has exactly one geocode, and every geocode
is associated with exactly one language.  If not, the ambiguities are
reported.  The CSV file must have the following columns:

    - "Unique Identifier"
    - "TYPE"
    - "GEO"

usage: geounique.py [<path_to_csv>.csv ...]
"""

import csv
import sys
import time
from collections import defaultdict

languages = defaultdict(set)
geocodes = defaultdict(set)

def report_inconsistencies():
    global languages
    global geocodes
    for lang in languages:
        geos = languages[lang]
        if len(geos) > 1:
            print("Language \"{}\" has multiple geocodes: {}".format(lang, ",".join(geos)))

    for geo in geocodes:
        langs = geocodes[geo]
        if len(langs) > 1:
            print("Geocode \"{}\" has multiple languages: {}".format(geo, ",".join(langs)))

def process_language(language, geocode):
    languages[language].add(geocode)
    geocodes[geocode].add(language)

def process_row(row):
    uuid = row.get("Unique Identifier") or "<unknown unique identifier>"
    geo = row.get("GEO CODE") or ""
    lang = row.get("Language") or ""

    #if lang and not geo:
    #    print("ID {} (language {}) missing geocode".format(uuid, lang))
    #if geo and not lang:
    #    print("ID {} (geocode {}) missing language".format(uuid, geo))

    if lang and geo:
        process_language(lang, geo)

def process_file(filename):
    with open(filename, newline='', encoding='utf-8-sig') as f:
        rows = csv.DictReader(f, quotechar='"', dialect='excel')
        n = 0
        for row in rows:
            process_row(row)
            n += 1
    return n

def main():

    n = 0
    b = time.time()
    for fn in sys.argv[1:]:
        print("Processing " + fn + "...")
        n += process_file(fn)
    e = time.time()

    report_inconsistencies()

    print("All done!")
    print("Processed {} entries in {:4.2f} seconds".format(n, (e-b)))

if __name__ == "__main__":
    main()
