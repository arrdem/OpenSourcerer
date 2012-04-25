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

    i, count = 0, db.cards.find().count()

    while(i < count):
        cursor = db.cards.find({}, {'name':1}).skip(i)

        for card in cursor:
            try:
                decks = db.decks_unrated.find({card['name']: {'$gt': 0}},
                                              {card['name']:1})

                s = 0
                c = 0
                for d in decks:
                    s += d[card['name']]
                    c += 1

                a = float(s)/float(c)

                if(c and s):
                    db.cards.update(
                        {'name': card['name']},
                        {'$set': {'decks': c, 'uses': s, 'avg count':a}})

                print("Done with card: %-25s    Uses: %-6i    Total: %-6i" %
                        (card['name'], c, s))
                i += 1

            except KeyError:
                print("Derped...")
            except Exception as e:
                print(e)

