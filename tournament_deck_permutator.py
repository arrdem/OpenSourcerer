#!/usr/bin/env python3
# -*- coding: utf-8 *-*
from pymongo.connection      import Connection
from configparser            import SafeConfigParser


parser = SafeConfigParser()
parser.read('settings.ini')
connection = Connection(parser.get('mongodb', 'server'))
db = None
exec('db = connection.' + parser.get('mongodb', 'db'))


def is_card_related(card, db):
    """
    Uses some heuristics and the Mongo DB to determine whether the card in
    question is or is not strongly correlated.
    """
    pass


def permutate(deck, db, mutation_rate=0.125):
    """
    This function takes a deck as an array of cards __excluding lands__ and
    replaces cards on a random basis with related cards. The idea is to achieve
    an incremental search of the deck space by exploring related or high
    correlation card pairs.
    """
    pass
