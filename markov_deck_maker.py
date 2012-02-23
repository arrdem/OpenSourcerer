#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  markovdeck.py

from lib.markov         import MarkovChain as mc
import os

if __name__ == "__main__" or 1:
    path = "./data/decks/"
    ai = mc()

    if True:
        # load the deck data. Yes all of it. In one go. I love Python...
        for deck in os.listdir(path):
            with open(path + deck) as f:
                cards = {}
                for line in f:
                    data = line.split(" ")
                    s = ' '.join(data[1::])
                    s = s.strip('\n')
                    s = s.strip('\r')
                    cards[s] = int(data[0])
                for c in cards:
                    for d in cards:
                        ai.add(c,d,value=cards[d])
    else:
        ai.load(open("./ai.conf"))

    deck = [ai.get() for i in range(60)]
    deck.sort()

    deck_clean = {}

    for c in deck:
        if c not in deck_clean:
            deck_clean[c] = 1
        else:
            deck_clean[c] += 1

    d2 = []
    for c in deck:
        if c not in d2:
            d2.append(c)
    d2.sort()

    for c in d2:
        print deck_clean[c], c
