#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cli.py
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

from .client        import Client
from .signal.event  import *
from .signal.turn   import *
from .signal.signal import *

class CLI(Client):
    name            = None
    deck            = None
    """
    Defines a simple command line interface for the engine
    """
    def __init__(self, gi, name):
        Client.__init__(self, gi)
        self.name = name

    def __str__(self):
        return name, helth

    def __handle__(self, sig):
        # this method is GURANTEED to recieve a signal, and is to be overridden
        # in every subclass.
        pass
