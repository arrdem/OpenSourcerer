#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       turn.py
#
#       Copyright 2012 Reid McKenzie <rmckenzie92@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

from .signal import Signal

class Turn(Signal):
    player  = None
    """
    This class serves as a base for all the signals which are specific
    to turn phases and events
    """
    def __init__(self, player):
        Signal.__init__(player)
        self.player = player

class Untap(Turn):
    """
    This class serves to signal the untap step of a player's turn
    """
    def __init__(self, player):
        Turn.__init__(player)

class Upkeep(Turn):
    """
    This class serves to signal the upkeep step of a player's turn
    """
    def __init__(self, player):
        Turn.__init__(player)

class Main(Turn):
    """
    This class serves to signal a player's main step (not needed?)
    """
    def __init__(self, player):
        Turn.__init__(player)

class Attack(Turn):
    """
    This class serves to signal a player's attack statement. Not sent
    if no attack is made.
    """
    def __init__(self, player):
        Turn.__init__(player)

class Block(Turn):
    """
    This class serves to signal a player's declaration of blockers.
    """
    def __init__(self, player):
        Turn.__init__(player)

class End(Turn):
    """
    This class serves to signal a player's end step.
    """
    def __init__(self, player):
        Turn.__init__(player)

class EndPhase(Turn):
    """
    This class serves to signal the end of a player's phase.
    """
    def __init__(self, player):
        Turn.__init__(player)
