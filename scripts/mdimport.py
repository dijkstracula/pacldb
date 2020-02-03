#!/usr/bin/env python3

"""
mdimport.py
author: Nathan Taylor <nbtaylor@gmail.com>

mdimport reads a directory of markdown files and inserts them
into the static_content table.

usage: csvmigrate.py <path-to-database> <path_to_markdowns>.
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


db_inserts = 0

def process_one(session, fn):
    name = os.path.basename(fn).split(".")[0]
    with open(fn) as f:
        text = f.read()

    sc = StaticContent(name=name, body_md=text)
    session.add(sc)
    session.commit()

def process_all(session):
    global db_inserts

    for fn in os.listdir(sys.argv[2]):
        print("Processing {}...".format(fn))
        fn = os.path.join(sys.argv[2], fn)
        if os.path.isfile(fn):
            process_one(session, fn)
            db_inserts += 1

def init_session(dbpath):
    engine = sqlalchemy.create_engine(dbpath)
    Session = sessionmaker(bind=engine)
    return Session()

def main():
    session = init_session(sys.argv[1])

    session.query(StaticContent).delete()
    session.commit()

    process_all(session)

    print("Added {} entries.".format(db_inserts))

if __name__ == "__main__":
    main()
