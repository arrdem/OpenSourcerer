#!/usr/bin/env python3
# -*- coding: utf-8 *-*
from McKenzieLib.tournament.scoring import BNet

names = ['reid', 'david', 'adam', 'dan', 'yo mamma', 'marci']
tourney = BNet(names, [1500] * len(names))

i = tourney.next()
while True:
    try:
        cmd = input('> ').split(' ', 1)
        if(cmd[0] in ('exit', 'quit')):
            print(tourney.getRankings())
            return

        elif(cmd[0] == 'next' or cmd[0] == ''):
            a, b = next(i)
            while True:
                print("1 - %s\n2 - %s" % (str(a), str(b)))
                c = int(input("choose 1 or 2 > "))
                if(c == 1):
                    tourney.logGame(a, b)
                    break
                elif(c == 2):
                    tourney.logGame(b, a)
                    break
                else:
                    continue
<<<<<<< HEAD
    except:
        pass
=======
    except Exception as e:
        print(e)
>>>>>>> retardation
