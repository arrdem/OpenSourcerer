#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from .signal.signal import Signal

class Client(object):
    __gameinstance__    = None
    """
    Serves to define the basic interface which all game clients will use to
    send a recieve signals.
    """
    def __init__(self, gi):
        self.__gameinstance__ = gi

    def __handle__(self, sig):
        # this method is GURANTEED to recieve a signal, and is to be overridden
        # in every subclass.
        pass

    def signal(self, sig):
        if(isinstance(sig, Signal)):
            # call the private metaprogrammed method which actually does the
            # leg work of handling signals
            self.__handle__(sig)
