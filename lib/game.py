#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   game.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

import random

from .client        import *
from .signal.signal import *
from .signal.turn   import *
from .player.player import Player
from .typedfunction import *


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

    @argtypes(object, Signal)
    def __handle__(self, sig):
        """
        Overrides the __handle__ method defined by the Client API
        """
        if isinstance(sig, EndPhase):
            pass

    @argtypes(object, Signal)
    def __broadcast__(self, sig):
        for c in self.signal_clients:
            c.signal(sig)

    @argtypes(object, Player)
    def addPlayer(self, p):
        self.players.append(p)
        self.signal_clients.append(p)

    @argtypes(object, Client)
    def addClient(self, c):
        self.signal_clients.append(c)

    @argtypes(object, Signal)
    def sendSignal(self, s):
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
