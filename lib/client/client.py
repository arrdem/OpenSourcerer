#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
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

from ..signal.signal import Signal

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
