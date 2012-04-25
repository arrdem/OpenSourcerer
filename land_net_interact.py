#!/usr/bin/env python2
# -*- coding: utf-8 *-*
from pymongo.connection             import Connection
from ConfigParser                   import SafeConfigParser
import lib.deck.deck as deck
import lib.ai.land_ai as ai
import pickle
import sys

if __name__ == '__main__':
    parser = SafeConfigParser()
    parser.read('settings.ini')

    connection = Connection(parser.get('mongodb', 'server'))
    db = None
    exec('db = connection.' + parser.get('mongodb', 'db'))

    net = pickle.load(open(parser.get('land_net', 'brain')))

    if '-d' in sys.argv:
        print "Input deck in the format [count] [card], ^d ends input"
        d = deck.parse('\n'.join(sys.stdin.readlines()))
        iv = ai.input_vector(d, db)

        print('-'*20)
        print(iv)
        print('-'*20)
        ai.print_output_vector(net.activate(iv))
        exit(0)

    else:
        while True:
            i = raw_input()
            print net.activate(map(float, i.split(' ')))

