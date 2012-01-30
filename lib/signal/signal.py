#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   signals.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

class Signal:
    """
    This class serves as the superclass for all events which the game
    needs to signal and deal with.
    """
    source  = None       # the source of the event

    def __init__(self, source):
        self.source = source

class Update(Signal):
    """
    This class causes EVERYTHING to update.
    """

    def __init__(self):
        Signal.__init__(None)
