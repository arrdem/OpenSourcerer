#!/usr/bin/env python
from __future__ import division
import mcardlib
import csv
import sys

_logfile = open("./name-errors.txt",'w')
_cards = mcardlib.load()
sys.stdout.write("[!] CARDS LOADED\n")

names = list(set([foo["Card Name:"] for foo in _cards]))
sys.stdout.write("[!] NAMES STRIPPED\n")
sys.stdout.write("[!] "+str(len(names))+" UNIQUE NAMES\n")

MUIDs = []
z = 0

for bar in range(len(names)):
    a = u''.join(["+["+i+"]" for i in unicode(names[bar]).split(" ")])
    try:
        MUIDs += [mcardlib.getMID(url="http://gatherer.wizards.com/Pages/Search/Default.aspx?name="+a)]
    except:
        print "\r[!] ERROR IN "+names[bar]
        _logfile.write(names[bar]+"\n")
        _logfile.flush()
    
    if z <= 50:
        sys.stdout.write("\r["+"="*z+">"+" "*(51-z)+"]  "+str(len(MUIDs))+" "+str((bar*100)/len(names)))
        sys.stdout.flush()
        z+=1
    else:
        z=0
    

of = open("./muids.dat",'w')
for id in MUIDs:
    of.write(str(id)+"\n")
