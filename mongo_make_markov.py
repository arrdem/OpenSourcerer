#!/usr/bin/env python2

from pymongo.connection import Connection
connection = Connection("146.6.213.39")
db = connection.magic

start = int(db.decks.find().count() * 0.0)
cursor = db.decks.find().skip(start)
c = start
while 1:
    try:
        for deck in cursor:
            print deck['_id'], float(c)/float(cursor.count())
            c += 1
            for c1 in deck:
                if c1 not in ['_id', 'name']:
                    duck = {k:deck[k] for k in deck if k not in ['name', '_id']}
                    duck['sum'] = sum([deck[k] for k in deck if k not in ['name', '_id']])
                    db.markov.update({'name':c1}, {'$inc': duck}, True)
                    #print("   ", c1, c2)
        exit(0)
    except:
        cursor = db.decks.find().skip(c) # continue from where the run failed


