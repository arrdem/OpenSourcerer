#!/usr/bin/env python3
# -*- coding: utf-8 *-*
from pymongo.connection import Connection
from configparser import SafeConfigParser

if __name__ == '__main__':
    global parser
    parser = SafeConfigParser()
    parser.read('settings.ini')

    connection = Connection(parser.get('mongodb', 'server'))
    db = None
    exec("db = connection." + parser.get('mongodb', 'db'))

    print("generating name set...")
    names = set(n['name'] for n in db.cards.find({}, {'name':1}))
    print("done!")

    print(type(names))
    print(names)

    for name in names:
        try:
            high = db.cards.find({"name": name},
                                 {"muid":1}).sort("muid",-1).limit(1)[0]['muid']

            dups = db.cards.find({'name': name, 'muid': {'$lt': high}}).count()

            db.cards.remove({'name': name, 'muid': {'$lt': high}})

            if(dups):
                print("removed %-3i duplicates of '%s'" % (dups, name))

        except KeyError:
            print("Derped...")
        except Exception as e:
            print(e)

