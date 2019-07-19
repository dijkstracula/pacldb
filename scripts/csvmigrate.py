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

usage: csvmigrate.py <path-to-database>.sqlite [<path_to_csv>.csv ...]
"""

import sqlite3
import csv
import os
import re
import string
import sys
import time

from collections import defaultdict

concepts = defaultdict(list)

class Migrator:
    def __init__(self, dbpath):
        if not os.path.isfile(dbpath):
            raise Exception("database {} not found".format(dbpath))

        self.conn = sqlite3.connect(dbpath)
        self.rows_processed = 0

        c = self.conn.cursor()
        c.execute('DELETE FROM concepts')
        c.execute('DELETE FROM terms')
        c.execute('DELETE FROM glosses')
        c.execute('DELETE FROM languages')

    def process_language(self, name, geocode):
        c = self.conn.cursor()
        c.execute('SELECT * FROM languages WHERE name=? AND geocode=?', (name, geocode))
        if len(c.fetchall()) > 0:
            return # Already exists.
        c.execute('INSERT INTO languages(name, geocode) VALUES (?,?)', (name, geocode))
        self.rows_processed += 1

    def process_concept(self, name, domain):
        c = self.conn.cursor()
        c.execute('SELECT * FROM concepts WHERE name=? AND domain=?', (name, domain))
        if len(c.fetchall()) > 0:
            return # Already exists.

        c.execute('INSERT INTO concepts(name, domain) VALUES (?,?)', (name, domain))
        self.rows_processed += 1

    def process_term(self, text, morph_type, cname, domain, geo):
        c = self.conn.cursor()
        c.execute('SELECT id FROM concepts WHERE name=? AND domain=?', (cname, domain))
        cid = c.fetchone()[0]

        if geo:
            c.execute('SELECT id FROM languages WHERE geocode=?', (geo,))
            lid = c.fetchone()[0]
        else:
            lid = None

        c.execute('SELECT * FROM terms WHERE text = ?', (text,))
        if len(c.fetchall()) > 0:
            return # Already exists.

        c.execute('INSERT INTO terms(text, morph_type, concept_id, language_id) VALUES (?,?,?,?)', (text, morph_type, cid, lid))
        self.rows_processed += 1

    def process_gloss(self, text, gloss, bib_src, page):
        c = self.conn.cursor()
        c.execute('SELECT id FROM terms WHERE text=?', (text,))
        tid = c.fetchone()[0]

        c.execute('INSERT INTO glosses(gloss, source, page, term_id) VALUES (?,?,?,?)', (gloss, bib_src, page, tid))
        self.rows_processed += 1


    def process_row(self, row):
        typ = row.get("TYPE")
        morph_type = row["Morphological Type: N, N-N, N-N-N, N-P, NMLZ, PRED, N-QUAL, In"]
        geo = row.get("GEO CODE")
        lang = row.get("Language").strip()
        concept = row.get("Concept").strip()
        term = row.get("Original Term").strip()
        glosses = row.get("Original Gloss").strip() # comma separated
        bib_src = row.get("Bib-Source").strip()
        pgn = row.get("Page number").strip()

        if concept and typ and term:
            self.process_language(lang, geo)
            self.process_concept(concept, typ)
            self.process_term(term,morph_type,concept,typ, geo)
            for gloss in set(re.split("[,;]\s*", glosses)):
                self.process_gloss(term, gloss, bib_src, pgn)

    def process_file(self, filename):
        with open(filename, newline='', encoding='utf-8-sig') as f:
            rows = csv.DictReader(f, quotechar='"', dialect='excel')
            n = 0
            for row in rows:
                self.process_row(row)
                n += 1
        return n

def main():

    m = Migrator(sys.argv[1])
    b = time.time()
    for fn in sys.argv[2:]:
        print("Processing " + fn + "...")
        m.process_file(fn)
        m.conn.commit()
    e = time.time()

    print("All done!")
    print("Processed {} entries in {:4.2f} seconds".format(m.rows_processed, (e-b)))

    m.conn.close()


if __name__ == "__main__":
    main()
