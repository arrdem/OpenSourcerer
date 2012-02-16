#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  markovdeck.py

from lib.markov import MarkovChain as mc
import os

if __name__ == "__main__" or 1:
    path = "./data/decks/"
    ai = mc()

    if not os.path.isfile("./ai.conf"):
        for deck in os.listdir(path):
            with open(path + deck) as f:
                cards = []
                for line in f:
                    data = line.split(" ")
                    for i in range(int(data[0])):
                        s = ' '.join(data[1::])
                        s = s.strip('\n')
                        s = s.strip('\r')
                        cards.append(s)

                for c in cards:
                    for d in cards:
                        ai.add(c, d)
    else:
        ai.load(open("./ai.conf"))

    #print ai

    deck = [ai.get() for i in range(80)]
    deck_clean = {}

    for c in deck:
        if c not in deck_clean:
            deck_clean[c] = 1
        else:
            deck_clean[c] += 1

    for c in deck_clean:
        print deck_clean[c], c

    ai.save(open("./ai.conf", 'w'))
