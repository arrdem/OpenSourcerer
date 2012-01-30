#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cli.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from .player            import Player
from ..signal.event     import *
from ..signal.turn      import *
from ..signal.signal    import *

class CLI(Player):
    """
    Defines a simple command line interface for the engine
    """
    def __init__(self, gi, name):
        Player.__init__(self, gi)

    def __handle__(self, sig):
        # this method is GURANTEED to recieve a signal, and is to be overridden
        # in every subclass.
        pass
