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

usage: csvmigrate.py <path-to-database> [<path_to_csv>.csv ...]
"""

import psycopg2
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

        self.conn = psycopg2.connect(dbpath)
        self.db_inserts = 0
        self.rows_read = 0
        self.rows_skipped = 0

        c = self.conn.cursor()
        c.execute('DELETE FROM concepts')
        c.execute('DELETE FROM terms')
        c.execute('DELETE FROM glosses')
        c.execute('DELETE FROM languages')

    def process_language(self, name, geocode):
        c = self.conn.cursor()

        c.execute('SELECT * FROM languages WHERE name=%s and geocode <>%s OR name<>%s and geocode=%s', (name,geocode,name,geocode))
        res = c.fetchall()
        if len(res) > 0:
            print("Multiple geo results ({}, {})".format(name, geocode), str(res))
            return

        # Use OR here because some languages don't have geocodes and vice versa
        res = c.execute('SELECT * FROM languages WHERE name=%s or geocode=%s', (name,geocode))
        res = c.fetchall()
        if len(res) > 0:
            return # Already exists.

        c.execute('INSERT INTO languages(name, geocode) VALUES (%s,%s)', (name, geocode))
        self.db_inserts += 1

    def process_domain(self, name):
        c = self.conn.cursor()
        c.execute('SELECT * FROM domains WHERE name=%s', (name, ))
        if len(c.fetchall()) > 0:
            return # Already exists.
        c.execute('INSERT INTO domains(name) VALUES (%s)', (name, ))

        self.db_inserts += 1

    def process_concept(self, name, domain):
        c = self.conn.cursor()

        c.execute('SELECT id FROM domains WHERE name=%s', (domain,))
        did = c.fetchone()[0]

        c.execute('SELECT * FROM concepts WHERE name=%s AND domain_id=%s', (name, did))
        if len(c.fetchall()) > 0:
            return # Already exists.


        c.execute('INSERT INTO concepts(name, domain_id) VALUES (%s,%s)', (name, did))
        self.db_inserts += 1

    def process_term(self, ortho, stem, ipa, morph_type, cname, domain, geo):
        c = self.conn.cursor()

        c.execute('SELECT id FROM concepts WHERE name=%s', (cname, ))
        cid = c.fetchone()[0]

        if geo:
            c.execute('SELECT id FROM languages WHERE geocode=%s', (geo,))
            lid = c.fetchone()[0]
        else:
            lid = ""

        c.execute('SELECT id FROM morphs WHERE name=%s', (morph_type,))
        mid = c.fetchone()[0]

        c.execute('SELECT * FROM terms WHERE orthography = %s', (ortho,))
        if len(c.fetchall()) > 0:
            return # Already exists.

        c.execute('INSERT INTO terms(orthography, stem_form, ipa, morph_id, concept_id, language_id) VALUES (%s,%s,%s,%s,%s,%s)', (ortho, stem, ipa, mid, cid, lid))
        self.db_inserts += 1


    def process_morph(self, morph_name):
        c = self.conn.cursor()
        c.execute('SELECT id FROM morphs WHERE name=%s', (morph_name,))
        if len(c.fetchall()) > 0:
            return # Already exists.)

        c.execute('INSERT INTO morphs(name) VALUES (%s)', (morph_name,));
        self.db_inserts += 1


    def process_gloss(self, ortho, gloss, bib_src, page):
        c = self.conn.cursor()

        try:
            page = int(page)
        except Exception as e:
            page = 0

        c.execute('SELECT id FROM terms WHERE orthography =%s', (ortho,))
        tid = c.fetchone()[0]

        c.execute('SELECT * FROM glosses WHERE gloss=%s AND source=%s AND page=%s', (gloss,bib_src, page))
        if len(c.fetchall()) > 0:
            return # Already exists.

        c.execute('INSERT INTO glosses(gloss, source, page, term_id) VALUES (%s,%s,%s,%s)', (gloss, bib_src, page, tid))
        self.db_inserts += 1


    def process_row(self, row):
        self.rows_read += 1

        domain = row.get("DOMAIN")
        morph_type = (row.get("Morphological Type: N, N-N, N-N-N, N-P, NMLZ, PRED, N-QUAL, In") or row.get("Morphological type") or "N/A").strip()
        geo = row.get("GEO CODE")
        lang = row.get("Language").strip()
        concept = row.get("Concept").strip()
        ortho = row.get("Orthography").strip()
        stem = row.get("Stem Form").strip()
        ipa = row.get("IPA Form").strip()
        glosses = row.get("Gloss").strip() # comma separated
        bib_src = row.get("Bib-Source").strip()
        pgn = row.get("Page number").strip()

        if concept and domain and ortho:
            self.process_domain(domain)
            self.process_language(lang, geo)
            self.process_concept(concept, domain)
            self.process_morph(morph_type)
            self.process_term(ortho, stem, ipa, morph_type,concept,domain, geo)

            for gloss in set(re.split("[,;]\s*", glosses)):
                self.process_gloss(ortho, gloss, bib_src, pgn)
        else:
            self.rows_skipped += 1

    def process_file(self, filename):
        with open(filename, newline='', encoding='utf-8-sig') as f:
            rows = csv.DictReader(f, quotechar='"', dialect='excel')
            n = 0
            for row in rows:
                try:
                    self.process_row(row)
                except Exception as e:
                    print(row)
                    raise e
                n += 1
                if (n % 100 == 0):
                    sys.stderr.write(".")
                    sys.stderr.flush()
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
    print("Inserted {} entries in {:4.2f} seconds".format(m.db_inserts, (e-b)))
    print("Skipped {}/{} rows.".format(m.rows_skipped, m.rows_read))
    m.conn.close()


if __name__ == "__main__":
    main()
