#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   card.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

class Card(object):
    """
    This object serves to represent a basic card/spell as it would be in
    a deck or hand. Because I already have the old mcardlib from the
    first downloader I'm going to do something stupid and dangerous here
    to initialize my class member variables:
        I am going to take a dict of card data in the constructor
        and I am going to UPDATE self.__dict__ LIKE A MOFO BAUS
    """

    def __init(self, d):
        self.__dict__.update(d)
