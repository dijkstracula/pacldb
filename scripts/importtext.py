#!/usr/bin/env python3

"""
importtext.py
author: Nathan Taylor <nbtaylor@gmail.com>


usage: csvmigrate.py <db_path> [<txt identifier> <path_to_txt>.txt]+
"""

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
from sqlalchemy.orm import sessionmaker
from app.models import StaticContent

concepts = defaultdict(list)

class Inserter:
    def __init__(self, dbpath):
        self.engine = sqlalchemy.create_engine(dbpath)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.db_inserts = 0

        self.session.query(StaticContent).delete()
        self.session.commit()

    def process_entry(self, name, text):
        sc = self.session.query(StaticContent).filter_by(name = name).all()
        if len(sc) > 0:
            raise Exception("{} already present".format(name))
        sc = StaticContent(name=name, text=text)
        self.session.add(sc)
        self.session.commit()
        self.db_inserts += 1

    def process_file(self, name, filename):
        with open(filename, newline='', encoding='utf-8-sig') as f:
            text = f.readlines()
            self.process_entry(name, text)

def main():

    inserter = Inserter(sys.argv[1])
    b = time.time()
    i = 2
    while i < len(sys.argv):
        name = sys.argv[i]
        fn = sys.argv[i+1]

        print("Processing {} {}...".format(name, fn))
        inserter.process_file(name, fn)
        i += 2

    e = time.time()

    print("All done!")
    print("Inserted {} entries in {:4.2f} seconds".format(inserter.db_inserts, (e-b)))


if __name__ == "__main__":
    main()
