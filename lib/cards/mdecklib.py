#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright Reid McKenzie, 2011
#
#   mdecklib is a suite I threw together to deal with loading and saving
#   decks in a standardized format. Because cards do vary by printing,
#   the format of a .deck file is [MUID],[NUMBER]\n.
#
#   However, decks can also be exported to a text file in the format
#   [NUMBER]x [CARD NAME]\n
#
#   It is important to note that the mdecklib.load() function returns
#   data of exactly the same format that mcardlib.load() does.
#   Just to make searching easy.

import mcardlib
import re
import os

_lib = mcardlib.load()

def load(filename):
    """Returns two dics. THe first maps card names to integer counts.
    The second maps Multiverse IDs to integer counts."""
    _if = open(filename)
    a,b = {},{}

    for line in _if:
        line = re.sub(re.compile("\s\n"),'',line)
        line = line.split(",")
        a[mcardlib.find(_lib,u"Multiverse ID:",int(line[0]))[0][u"Card Name:"]] = int(line[1])
        b[int(line[0])] = int(line[1])

    return a,b

def save(filename, data, mode = ".deck"):
    """Saves the data itterable. Data format will be adjusted for, but
    must be one of the two formats returned by load()."""
    types = [type(a) for a in data]
    of = open(filename,'w')

    _o=lambda x,y: str(x)+","+str(y)+"\n"
    _od = []

    if mode == ".deck":
        if unicode in types:
            for key in data:
                print key, data[key]
                print mcardlib.search(_lib,u"Card Name:",key)[0]
                of.write(_o(data[key],mcardlib.search(_lib,u"Card Name:",key)[0][u"Multiverse ID:"]))

        else:
            # just go ahead and write 'em out
            _od = [_o(key, data[key]) for key in data]
    else:
        # format is name, count not MUID, count
        if unicode in types:
            _od = [_o(key, data[key]) for key in data]

        else:
            # just go ahead and write 'em out
            for key in data:
                print key, data[key]
                of.write(_o(key,mcardlib.search(_lib,u"Multiverse ID:",key)[0][u"Card Name:"]))

def import_deck(filename):
    """Import takes a .txt file of the format [COUNT]<SPACE>[NAME],
    converts it to the .deck format and returns the product of loading
    the converted file."""
    s = u''.join(open(filename))
    s = re.sub(re.compile("^[0-9]*?x? *[A-Za-z]*?$"),'',s)
    s = re.sub(re.compile("  "),' ',s)
    s = [[i[0:i.find(" ")],i[i.find(" ")+1::]] for i in s.split("\n")]

    a = {}
    for i in range(len(s)):
        print repr(s[i])
        try:
            a[s[i][1]] = int(s[i][0])
        except:
            pass

    save(os.path.splitext(filename)[0]+".deck", a)

    return load(os.path.splitext(filename)[0]+".deck")

#print import_dk("./chandra.txt")
