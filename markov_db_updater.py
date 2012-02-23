#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  markovdeck.py

from pymongo.connection import Connection
import re
import os

if __name__ == "__main__" or 1:
    connection = Connection("146.6.213.39")
    db = connection.magic

    path = "./data/scraped_decks/"

    # load the deck data and upload it. Yes all of it. In one go. I love Python...
    for deck in os.listdir(path):
        with open(path + deck) as f:
            print ("Parsing deck %s..." % (deck))
            cards = {}
            for line in f:
                if not "//" in line and line:
                    data = line.split(" ")
                    s = ' '.join(data[1::])
                    s = s.strip('\n')
                    s = s.strip('\r')
                    try:
                        cards[s] = int(data[0])
                    except Exception:
                        print ("ERROR: \"%s\"" % line)
                else:
                    continue
            for c in cards:
                for d in cards:
                    # increment the counter for (c, d)
                    print ("    Updating (%s, %s, +1)" % (c, d))
                    db.markov.update({'name':c}, {"$inc":{d:1, 'sum':1}}, upsert=True)
