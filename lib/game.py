#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
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

from .client.client import *
from .signal.signal import *
from .signal.turn   import *
#TODO add a Player class

class GameInstance(Client):
    players             = []        # list of all players
    active_player       = None      # the active player
    signal_clients      = []        # list of all things which get signals
    spell_stack         = []        # spell stack

    __phases__          = []        # list of all turn phases
    __sig_stack__       = []        # stack of signals
    __phasegen__        = None      # a generator object of turn phase signals
    __playergen__       = None      # a generator object of players

    """
    Serves to manage, signal all the game events and turns.
    """

    def __init__(self):
        Client.__init__(self, self)
        self.players        = []
        self.active_player  = None
        self.signal_clients = [self]

        self.__sig_stack__  = []
        self.__phases__     = [Untap, Upkeep, Main, Attack, Main, End]

        self.__phasegen__   = self.__make_generator__(self.__phases__)
        self.__playergen__  = self.__make_generator__(self.players)

    def __make_generator__(self, i):
        while 1:
            for x in i:
                yield x

    def __handle__(self, sig):
        """
        Overrides the __handle__ method defined by the Client API
        """
        if isinstance(sig, EndPhase):
            pass

    def __broadcast__(self, sig):
        for c in self.signal_clients:
            c.signal(sig)

    def addPlayer(self, p):
        if(isinstance(p, Player)):
            players.append(p)
            signal_clients.append(p)
        else:
            raise TypeError("Can only add players or subclasses thereof")

    def addClient(self, c):
        if(isinstance(c, Client)):
            signal_clients.append(c)
        else:
            raise TypeError("Only clients or subclasses of client can be added")

    def sendSignal(self, s):
        if(isinstance(s, Signal)):
            self.__sig_stack__.append(s)

    def run(self):
        """
        Defines the game loop
        """
        random.shuffle(self.players)

        while [p for p in self.players if p.isActive()]:
            for player in self.__playergen__:
                if player.isActive():
                    for phase in self.__phases__:
                        self.__broadcast__(phase(player))

                        while self.__sig_stack__:
                            s = self.__sig_stack__.pop(0)
                            if isinstance(s, EndPhase):
                                break
                            else:
                                self.__broadcast__(s)
