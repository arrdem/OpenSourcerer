#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  markovdeck.py

from lib.markov.mongo_markov import MongoMarkovChain as mc
from pymongo.connection import Connection
from collections import defaultdict as bag
import cProfile

def main():
    connection = Connection("146.6.213.39")
    db = connection.magic
    ai = mc(db, "markov", exp=1.2)

    deck = []

    for i in range(100):
        c = ai.get()
        if(isinstance(c, type(""))):
            deck.append(c)

    deck.sort()

    deck_clean = bag(lambda: 0)

    for c in deck:
        deck_clean[c] += 1

    for c in set(deck):
        print ("%2i  %s" % (deck_clean[c], c))

if __name__ == "__main__":
    main()
#    cProfile.run('main()')
