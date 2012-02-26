#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   main.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.
from lib.game              import GameInstance as GI
from lib.player.player   import Player
from lib.signal.event    import *
from lib.signal.turn      import *
import re

if __name__ == "__main__" or 1:
    m = {}
    for name in dir():
        a = re.match("__", name)
        if a is None:
            exec("m[name] =" + name)

    game = GI()
    p = Player(game, [], "me")
    game.addPlayer(p)

    while True:
        c = input("$ ").split(" ")

        if(c[0] == "signal"):
            pass

        elif(c[0] == "help"):
            if(len(c) == 1):
                print("Available Signals")
                for a in m:
                    print("    " + a)

            else:
                print("Type data for %s" % c[1])
                exec("a = " + c[1] + ".__init__")


                if(a.__arg_types__):
                    print("__arg_types__:")
                    for t in a.__arg_types__:
                        print("    " + str(t))

                if(a.__kwarg_types__):
                    print("__kwarg_types__:")
                    for t in a.__kwarg_types__:
                        print("    " + t)

        elif(c[0] == "send"):
            c = ' '.join(c[1::])
            print("Exec string: " + c)
            s = exec(c)
            exec(game.sendSignal(s))

        elif(c[0] == 'exit'):
            exit(0)

        else:
            try:
                exec(' '.join(c))
            except:
                pass
