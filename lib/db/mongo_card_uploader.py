#!/usr/bin/env python
from pymongo.connection import Connection

for line in open("cards.dat"):
    d = None 
    exec("d = "+line)
    print(d['
