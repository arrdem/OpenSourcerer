#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo.connection import Connection
connection = Connection("146.6.213.39")
db = connection.magic

start = 0  # int(db.decks.find().count() * 0.416653800017)
cursor = db.decks.find().skip(start)
c = start
while 1:
    try:
        for deck in cursor:
            print deck['_id'], float(c) / float(cursor.count())
            c += 1
            duck = {k: deck[k] for k in deck if k not in ['name', '_id']}
            db.markov.update({'name': {"$in": [k for k in deck
                                                if k not in ['_id', 'name']]}},
                             {'$inc': duck}, True)
        exit(0)
    except:
        cursor = db.decks.find().skip(int(c))


