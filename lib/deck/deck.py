#!/usr/bin/env python
# -*- coding: utf-8 *-*
from collections import defaultdict as bag
import re

class Deck:
    def __init__(self, deck={}):
        self.__deck__  = deck
        self.__count__ = bag(lambda: 0)

    def __getitem__(self, key):
        if key in self.__deck__:
            return self.__deck__[key]
        else:
            return None

    def parse(self, s):
        b = bag(lambda: 0)
        s = re.sub(r'\r\n', '\n', s)
        lines = re.split(r'\n', s)

        for l in lines:
            m = re.match('//', l)
            if m is None:
                l = re.sub(r'SB:  ', '', l)
                l = re.sub(r' +', ' ', l)
                l = re.sub(r'^ +', '', l)
                l = l.split(" ")
                card_name = ' '.join(l[1::])
                count = l[0]

                if(verbose): print(l,  card_name,  count)
                if l and (not False in [bool(a) for a in l]):
                    try:
                        s = ' '.join(l[1::]).strip('.')
                        b[s] += int(l[0])

                    except:
                        raise ParseError("Unable to parse the deck")

        b['sum'] = sum(b[i] for i in b if isinstance(b[i], int))

        self.__count__ = deck

        return deck

    def export(self):
        buff = ""
        for c in self.__count__:
            buff += "%i %s\n" % (self.__count__[c], c)
        return buff

    def statistics(self, db):
        cards = [db.cards.find({'name':c}).limit(1)[0] for c in self.__count__]

        mana_curve = bag(lambda: 0)
        for c in cards:
            mana_curve[sum(c["cost"][a] for a in c["cost"])] += 1

        types = bag(lambda: 0)
        for c in cards:
            types[c["types"][0]] += 1
