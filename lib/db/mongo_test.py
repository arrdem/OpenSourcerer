#!/usr/bin/env python

from pymongo import Connection

db = Connection('localhost', 27017)
cards = db.cards
print cards.find()
print type(cards)
cards.insert({'name':'ogre', 'power':4, 'toughness':3, 'cost':[0,3,2,0,0,0]})
print cards.find()

