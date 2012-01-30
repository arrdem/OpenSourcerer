#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   turn.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

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

    def __str__(self):
        return "Turn generic signal"

class Untap(Turn):
    """
    This class serves to signal the untap step of a player's turn
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "Untap phase signal"

class Upkeep(Turn):
    """
    This class serves to signal the upkeep step of a player's turn
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "Upkeep phase signal"

class Main(Turn):
    """
    This class serves to signal a player's main step (not needed?)
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "Main phase signal"

class Attack(Turn):
    """
    This class serves to signal a player's attack statement. Not sent
    if no attack is made.
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "Attack phase signal"

class Block(Turn):
    """
    This class serves to signal a player's declaration of blockers.
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "Blocking phase signal"

class End(Turn):
    """
    This class serves to signal a player's end step.
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "End phase signal"

class EndPhase(Turn):
    """
    This class serves to signal the end of a player's phase.
    """
    def __init__(self, player):
        Turn.__init__(player)

    def __str__(self):
        return "End of phase signal"
