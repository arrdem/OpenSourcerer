#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  player.py
#
#  Copyright 2012 Reid McKenzie <rmckenzie92@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import random
from .client.client import Client

class Player(object):
    deck        = None
    hand        = None
    permanents  = None
    life        = None
    nic         = None

    """
    Player serves as a base class for all game players local, remote, human and
    other.
    """

    def __init__(self, deck, name, life=20):
        self.nic    = name
        self.deck   = deck
        self.life   = life
        self.hand   = []

        random.shuffle(self.deck)
        self.draw(n=7)

    def draw(self, n=1):
        for i in range(n):
            self.hand.append(self.deck.pop())

