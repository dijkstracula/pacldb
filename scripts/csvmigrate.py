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

import csv
import os
import re
import string
import sys
import time

from collections import defaultdict

# path hack to import app.model; I hate this
import sys, os
sys.path.insert(0, os.path.abspath('.'))

import sqlalchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from app.models import *

class Migrator:
    def __init__(self, dbpath):
        self.engine = sqlalchemy.create_engine(dbpath)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.db_inserts = 0
        self.rows_read = 0
        self.rows_skipped = 0

        self.session.query(Gloss).delete()
        self.session.query(Term).delete()
        self.session.query(Domain).delete()
        self.session.query(Morph).delete()
        self.session.query(Language).delete()
        self.session.commit()

    def process_language(self, name, geocode):
        #'SELECT * FROM languages WHERE name=%s and geocode <>%s OR name<>%s and geocode=%s', (name,geocode,name,geocode)
        res = self.session.query(Language).filter(or_(
            and_(Language.name==name, Language.geocode!=geocode),
            and_(Language.name!=name, Language.geocode==geocode))).all()
        if len(res) > 0:
            raise Exception("Multiple geo results ({}, {})".format(name, geocode))

        # Use OR here because some languages don't have geocodes and vice versa
        #'SELECT * FROM languages WHERE name=%s or geocode=%s', (name,geocode)
        res = self.session.query(Language).filter(
            or_(Language.name==name, Language.geocode==geocode)).all()
        if len(res) > 0:
            return # Already exists.

        #'INSERT INTO languages(name, geocode) VALUES (%s,%s)', (name, geocode)
        l = Language(name=name, geocode=geocode)
        self.session.add(l)
        self.db_inserts += 1

    def process_domain(self, name):
        #'SELECT * FROM domains WHERE name=%s', (name, )
        res = self.session.query(Domain).filter_by(name=name).all()
        if len(res) > 0:
            return # Already exists.

        d = Domain(name=name)
        self.session.add(d)

        self.db_inserts += 1

    def process_term(self, ortho, stem, ipa, morph, cname, domain, geo):

        res = self.session.query(Term).filter_by(orthography=ortho).all()
        if len(res) > 0:
            #raise Exception("Duplicate orthography")
            return

        domain = self.session.query(Domain).filter_by(name=domain).first()
        lang = self.session.query(Language).filter_by(geocode=geo).first()
        morph = self.session.query(Morph).filter_by(name=morph).first()

        if not domain:
            raise Exception("Missing domain")
        if not lang:
            raise Exception("Missing lang")
        if not morph:
            raise Exception("Missing morph")

        #'INSERT INTO terms(orthography, stem_form, ipa, morph_id, concept_id, language_id) VALUES (%s,%s,%s,%s,%s,%s)', (ortho, stem, ipa, mid, cid, lid)
        term = Term(domain=domain,
                    concept=cname,
                    orthography=ortho,
                    stem_form=stem,
                    ipa=ipa,
                    morph=morph,
                    language=lang)
        self.session.add(term)
        self.db_inserts += 1


    def process_morph(self, morph_name):
        morph = self.session.query(Morph).filter_by(name=morph_name).first()
        if morph:
            return

        morph = Morph(name=morph_name)
        self.session.add(morph)
        self.db_inserts += 1


    def process_gloss(self, ortho, gloss, bib_src, page):
        try:
            page = int(page)
        except:
            page = 0

        #'SELECT * FROM glosses WHERE gloss=%s AND source=%s AND page=%s', (gloss,bib_src, page)
        res = self.session.query(Gloss).filter_by(gloss=gloss, source=bib_src, page=page).all()
        if len(res) > 0:
            return # Already exists.

        #'SELECT id FROM terms WHERE orthography =%s', (ortho,)
        term = self.session.query(Term).filter_by(orthography=ortho).first()
        if not term:
            raise Exception("Expected existing Term for orthography {}".format(ortho))

        #'INSERT INTO glosses(gloss, source, page, term_id) VALUES (%s,%s,%s,%s)', (gloss, bib_src, page, tid)
        g = Gloss(gloss=gloss, source=bib_src, page=page, term=term)
        self.session.add(g)
        self.db_inserts += 1


    def process_row(self, row):
        self.rows_read += 1

        domain = row.get("DOMAIN")
        morph = (row.get("Morphological Type: N, N-N, N-N-N, N-P, NMLZ, PRED, N-QUAL, In") or row.get("Morphological type") or "N/A").strip()
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
            self.process_morph(morph)
            self.process_term(ortho, stem, ipa, morph,concept,domain, geo)

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
                    self.session.commit()
                except Exception as e:
                    self.session.rollback()
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
    e = time.time()

    print("All done!")
    print("Inserted {} entries in {:4.2f} seconds".format(m.db_inserts, (e-b)))
    print("Skipped {}/{} rows.".format(m.rows_skipped, m.rows_read))


if __name__ == "__main__":
    main()
