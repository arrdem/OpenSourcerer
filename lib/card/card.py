#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   card.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from ..client import Client 

keys = [u"Card Name:", u"Mana Cost:", u"Converted Mana Cost:",
        u"Types:", u"Card Text:", u"Flavor Text:", u"P/T:", 
        u"Expansion:", u"Rarity:", u"Artist:", u"Community Rating:",
        u"Hand/Life:", u"Loyalty:", u"Multiverse ID:", 
        u'Community Votes:', u'Meta Rating:', u"Img File:", 
        u"Img MD5Sum:" ]

keywords = ['Absorb','Affinity','Amplify','Annihilator','Attach',
    'Aura swap','Banding','Bands with other','Bloodthirst','Bury','Bushido',
    'Buyback','Cascade','Champion','Changeling','Channel','Chroma','Clash',
    'Conspire','Convoke','Counter','Cumulative Upkeep','Cycling',
    'Deathtouch','Defender','Delve','Devour','Domain','Double strike',
    'Dredge','Echo','Enchant','Entwine','Epic','Equip','Evoke','Exalted',
    'Exile','Fading','Fateseal','Fear','First strike','Flanking','Flash',
    'Flashback','Flying','Forecast','Fortify','Frenzy','Graft','Grandeur',
    'Gravestorm','Haste','Haunt','Hellbent','Hexproof','Hideaway',
    'Horsemanship','Imprint','Infect','Intimidate','Join forces','Kicker',
    'Kinship','Landfall','Swampwalk','Islandwalk','Mountainwalk',
    'Forestwalk','Planeswalk','Landwalk','Swamphome','Islandhome',
    'Mountainhome','Foresthome','Planeshome','Landhome','Level up',
    'Lifelink','Madness','Metalcraft','Modular','Morph','Multikicker',
    'Ninjutsu','Offering','Persist','Phasing','Poisonous','Protection',
    'Provoke','Prowl','Radiance','Rampage','Reach','Rebound','Recover',
    'Regenerate','Reinforce','Replicate','Retrace','Ripple','Sacrifice',
    'Scry','Shadow','Shroud','Soulshift','Splice','Split second','Storm',
    'Substance','Sunburst','Suspend','Sweep','Tap','Threshold','Kicker',
    'Trample','Transfigure','Transmute','Totem armor','Unearth','Untap',
    'Vanishing','Vigilance','Wither']

class Card(Client):
    __handlers__        = None
    __status__          = 0     # 0: deck, 1: hand, -1: Gyard, -2: exile
    """
    This object serves to represent a basic card/spell as it would be in
    a deck or hand. Because I already have the old mcardlib from the
    first downloader I'm going to do something stupid and dangerous here
    to initialize my class member variables:
        I am going to take a dict of card data in the constructor
        and I am going to UPDATE self.__dict__ LIKE A MOFO BAUS
    """

    def __init__(self, gi, d):
        Client.__init__(self, gi)
        self.__dict__.update(d)
        self.__handlers__ = {}

    def __handle__(self, sig):
        if(sig.__class__ in self.__handlers__):
            f = self.__handlers__[sig]
            f(self, sig)

    def __null__(self, sig):
        return

    def __add_handler_method__(self, sig, handler):
        self.__hanlers__[sig.__class__] = setattr(self,
                                             func.__name__,
                                             types.MethodType(handler, self)
                                            )
