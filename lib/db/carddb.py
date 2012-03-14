#!/usr/bin/env python3

from ..cards.card import Card

class CardDB():
    def __init__(self, file='./cards.dat'):
        self.__cards__           = []    # list of Card objects
        self.__names_to_inst__   = {}    # map of '':Card

        f = open(file,'r')
        for line in f:
            try:
                eval("d = "+line)
                d = Card(None, d)
                self.__cards__.append(d)
                self[d.__dict__['Card Name:']] =  len(self.__cards__

            except Exception:
                continue

    def __contains__(self, element):
        """element is assumed to be the name of a card, or a card instance"""
        return ((element in self.__names_to_int__)
                or (element in self.__cards__))

    def __getitem__(self, addr):
        """addr is assumed to be a valid card name"""
        if addr in self.__names_to_ind__:
            return self.__cards__[self.__names_to_ind__[addr]]
        else:
            return None

    def __setitem__(self, addr, value):
        """addr is assumed to be a valid card name, value a card instance"""
        self.__cards__.append(value)
        self.__names_to_ind__[u'Card Name:'] = len(self.__cards__)

    def search(self, prop, value):
        return [c for c in self.__cards__
                    if (prop in c.__dict__ and c.__dict__[prop] == value)]


