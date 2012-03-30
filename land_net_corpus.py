# -*- coding: utf-8 *-*
from pymongo.connection             import Connection
from McKenzieLib.util.wrappers      import retlen
from McKenzieLib.util.iterators     import mix
from itertools                      import product
from ConfigParser                   import SafeConfigParser
import lib.ai.land_ai as ai
import pickle
import sys


if __name__ == '__main__':
    parser = SafeConfigParser()
    parser.read('settings.ini')

    connection = Connection(parser.get('mongodb', 'server'))
    db = None
    exec('db = connection.' + parser.get('mongodb', 'db'))

    f = open(parser.get('land_net', 'corpus')+'.'+sys.argv[1], 'w')

    lim = {'$gt': 8}
    count_per_type = int(sys.argv[1])

#    black = db.decks.find({'Swamp':    lim}).limit(count_per_type)
#    blue  = db.decks.find({'Island':   lim}).limit(count_per_type)
#    green = db.decks.find({'Forest':  lim}).limit(count_per_type)
#    red   = db.decks.find({'Mountain': lim}).limit(count_per_type)
#    white = db.decks.find({'Plains':   lim}).limit(count_per_type)

    t = (db.decks.find({e: lim for e in p}).limit(count_per_type)
                 for p in product(ai.__lands__, repeat=2))

    cursor = mix(*t)

    c = 0
    for d in cursor:
        try:
            i, o = ai.input_vector(d, db), ai.output_vector(d)
            f.write(ai.export_vector(i)+'|'+ai.export_vector(o)+'\n')
            print c
            c += 1
        except Exception as e:
            print e
            continue

    f.close()
