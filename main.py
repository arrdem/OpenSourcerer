#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   main.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from lib.game import GameInstance as GI
from lib.player import Player

if __name__ == "__main__" or 1:
    game = GI()
    p = Player([], "me")
    game.addPlayer(p)
