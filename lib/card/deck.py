#!/usr/bin/env python
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

import random
#TODO - add imports for Creature, Land, Spell, Plainswalker, Artifact

class Deck(list):
    __player__  = None
    """This class provides a step up in terms of code structur from using raw
       lists as a deck.
    """

    def __init__(self, plyr):
        list.__init__(self)
        self.__player__ = plyr
        random.shuffle(self)

    def scry(self, n=3):
        l = self[0:n]
        self = self[n::]
        return l

    def scry_push(self, l):
        self.__list__ = l + self

    def shuffle(self):
        random.shuffle(self)

    def search(self, i, v):
        for j in range(len(i)):
            if i[j] == v:
                return j
        return -1

    def set(self):
        return set(self)

    def tutor(self, card):
        if card in self:
            return self.pop(self.search(self, card))

    def push(self, i):
        self.append(i)

    def rate(self):
        pass

    def __str__(self):
        """I'll provide an implimentation for this later, but basically it
        should print out the deck in the same format as the text files I used
        to store the decks themselves."""
        return "Not Done Yet"
