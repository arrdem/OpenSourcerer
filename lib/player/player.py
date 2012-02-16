#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  player.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

import random
from ..client import Client

class Player(Client):
    deck        = []
    hand        = []
    permanents  = []
    graveyard   = []

    hand_size   = 7
    life        = 20
    nic         = None

    """
    Player serves as a base class for all game players local, remote, human and
    other.
    """

    def __init__(self, gameinstance, deck, name, life=20):
        Client.__init__(self, gameinstance)

        self.nic    = name
        self.deck   = deck
        self.life   = life
        self.hand   = []

        random.shuffle(self.deck)
        #self.draw(n=7)

    def __handle__(self, sig):
        """
        This method is inherited from Client and defines how the Player deals
        with all the signals which it may be sent by the system. MUST BE
        IMPLEMENTED IN ALL SUBCLASSES (this one gets a pass because it is an
        interface)
        """
        pass

    def __str__(self):
        return name, life

    def draw(self, n=1):
        """
        And just to make things idiot-proof...
        """
        for i in range(n):
            self.hand.append(self.deck.pop())

    def discard(self, n=1):
        """
        This is a placeholder method which __must__ be provided by any/all
        implementations of Player due to the 7 card hand cap (special cases
        provided for)
        """
        pass

