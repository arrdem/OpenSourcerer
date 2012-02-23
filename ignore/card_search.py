#!/usr/bin/env python

import mcardlib
from card_viewer import card_viewer

_cards = mcardlib.load(file ='./cards.dat')
Any = mcardlib.Any

_Header = """-----------------------------------------------------------------------
|                          Card Search                                |
-----------------------------------------------------------------------
"""

_Menu = ''.join([str(i)+"   -"+" "*(6-len(str(i)))+str(mcardlib._Keys[i])+"\n" for i in range(len(mcardlib._Keys))])+"""
NOTE: the value Any is used to match anything.
"""

print _Header, _Menu

while True:
    try:
        c = mcardlib._Keys[int(raw_input( "[  MENU  ] > "))]
    except ValueError:
        print _Menu
        continue
    except KeyboardInterrupt:
        print
        exit(0)
    except EOFError:
        print
        exit(0)
        
    i = eval(raw_input("[  KEY   ] > "))
    results = mcardlib.search(_cards, c, i)
    
    if c != 0:
        for foo in results:
            app = card_viewer(None)
            app.set(foo)
            app.mainloop()
            del app
    else:
        print repr(results[0])
