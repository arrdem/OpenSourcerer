#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   card.py
#
#   Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#   This code and all other code in the project may be used
#   or re-used for any purpose at all, so long as I am
#   made aware of my contribution.

from ..client import Client
from ..db.card_parser import *
from collections import defaultdict as dd
import re
import string

class Card(Client):

    __handlers__   = None
    __status__     = 0     # 0: deck, 1: hand, -1: Gyard, -2: exile
    __fields__     = ['name', 'cost', 'types', 'text', 'flavor_text',
                      'text_divs', 'keywords', 'power', 'toughness', 'rarity',
                      'expansion', 'muid', 'use_count', 'deck_count',
                      'loyalty', 'rating', 'img', 'meta', 'actions']

    __keywords__   = ["Absorb", "Affinity", "Amplify", "Annihilator", "Attach",
                      "Aura swap", "Banding", "Bands with other",
                      "Bloodthirst", "Bury", "Bushido", "Buyback", "Cascade",
                      "Champion", "Changeling", "Channel", "Chroma", "Clash",
                      "Conspire", "Convoke", "Counter", "Cumulative Upkeep",
                      "Cycling", "Deathtouch", "Defender", "Delve", "Devour",
                      "Domain", "Double strike", "Dredge", "Echo", "Enchant",
                      "Entwine", "Epic", "Equip", "Evoke", "Exalted", "Exile",
                      "Fading", "Fateseal", "Fear", "First strike", "Flanking",
                      "Flash", "Flashback", "Flying", "Forecast", "Fortify",
                      "Frenzy", "Graft", "Grandeur", "Gravestorm", "Haste",
                      "Haunt", "Hellbent", "Hexproof", "Hideaway",
                      "Horsemanship", "Imprint", "Infect", "Intimidate",
                      "Join forces", "Kicker", "Kinship", "Landfall",
                      "Swampwalk", "Islandwalk", "Mountainwalk", "Forestwalk",
                      "Planeswalk", "Landwalk", "Swamphome", "Islandhome",
                      "Mountainhome", "Foresthome", "Planeshome", "Landhome",
                      "Level up", "Lifelink", "Madness", "Metalcraft",
                      "Modular", "Morph", "Multikicker", "Ninjuts", "Offering",
                      "Persist", "Phasing", "Poisonous", "Protection",
                      "Provoke", "Prowl", "Radiance", "Rampage", "Reach",
                      "Rebound", "Recover", "Regenerate", "Reinforce",
                      "Replicate", "Retrace", "Ripple", "Sacrifice", "Scry",
                      "Shadow", "Shroud", "Soulshift", "Splice",
                      "Split second", "Storm", "Substance", "Sunburst",
                      "Suspend", "Sweep", "Tap", "Threshold", "Kicker",
                      "Trample", "Transfigure", "Transmute", "Totem armor",
                      "Unearth", "Untap", "Vanishing", "Vigilance", "Wither"]

    __gatherer_html_ids__ = \
    ['ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_setRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_totalVotes',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_playerRatingRow',
     'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage',
     ]

    """
    This object serves to represent a basic card/spell as it would be in
    a deck or hand. Because I already have the old mcardlib from the
    first downloader I'm going to do something stupid and dangerous here
    to initialize my class member variables:
        I am going to take a dict of card data in the constructor
        and I am going to UPDATE self.__dict__ LIKE A MOFO BAUS
    """

    def __init__(self, gi):
        Client.__init__(self, gi)
#        self.__dict__.update(d)
        self.__handlers__ = {}
        self.__record__   = {}

        for f in self.__fields__:
            setattr(self, f, 0)

    def __handle__(self, sig):
        if(sig.__class__ in self.__handlers__):
            f = self.__handlers__[sig]
            f(self, sig)

    def __null__(self, sig):
        return

    def __add_handler_method__(self, sig, handler):
        self.__hanlers__[sig.__class__] = setattr(self,
                                             func.__name__,
                                             types.MethodType(handler, self))

    def __getitem__(self, key):
        if key in self.__record__:
            return self.__record__[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.__record__[key] = value

    def export(self):
        return {field:self.__dict__[field] for field in self.__fields__}

    def loadFromGatherer(self, html):
        tree = None
        try:
            html = ''.join([c for c in html if c in string.printable])
            p = WebPage()
            p.feed(html)
            tree = p.__tree_root__

            # limit the syntax tree to the subtree making up the right column

            # first get the easy stuff...
            ## get the card's name
            res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_nameRow'))
            res = next(res.find(lambda x: x['class'] == 'value'))
            self.name = res['data'].strip()

            ## get the card's flavor text
            try:
                res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_FlavorText'))
                self.flavor_text = res.join().strip()
            except StopIteration as e:
                print(e)
                self.flavor_text = "None"

            ## get the card's core text
            self.text_divs = []
            try:
                res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'))
                res = res.__children__[1]
                self.text = ""
                for c in res.__children__:
                    t = c.__fields__['data'].strip()
                    if t:
                        self.text += (t + '\n')
                        self.text_divs.append(t)
            except StopIteration:
                self.text = "None"

            ## get the card's abilities/effects
            self.actions = []

            res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_textRow'))
            for a in self.text_divs:
                a = re.sub(r'[\n \t]', ' ', a)

                if (':' in a) or ('when' in a.lower()) or ('if ' in a.lower()) or ('may' in a.lower()):
                    self.actions.append(tuple(map(lambda x: x.strip(), a.split(':'))))

            ## get the card's types
            res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_typeRow'))
            res = next(res.find(lambda x: x['class'] == 'value'))
            self.types = [''.join(filter(lambda x:(0 <= ord(x) <= 128), s.strip())) for s in res['data'].split('—')]

            # now for the stuff which needs a little processing...
            ## get the power and toughness
            try:
                res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ptRow'))
                res = next(res.find(lambda x: x['class'] == 'value'))
                self.power, self.toughness = (int(s) for s in re.split('[\\/]',res['data'].strip()))
            except StopIteration:
                self.power, self.toughness = -1,-1

            ## get the mana cost
            self.cost = dd(lambda: 0)
            self.cost['X'] = False

            try:
                res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_manaRow'))
                res = next(res.find(lambda x: x['class'] == 'value'))

                for child in res.__children__:
                    try:
                        i = int(child.__fields__['alt'])
                        self.cost['*'] = i
                    except:
                        s = child.__fields__['alt']
                        if " or " in s:
                            s = (s[0].lower()) + "/" + (s.split(" ")[2][0].lower())
                        elif "Phyrexian" in s:
                            s = s.split(' ')[1]
                            self.cost['Phyrexian'] += 1

                        elif 'Variable Colorless' == s:
                            self.cost['X'] = True
                            continue

                        self.cost[s] += 1
            except StopIteration:
                pass

            self.cost = {k: self.cost[k] for k in self.cost}

            ## get the converted cost row
            res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cmcRow'))
            res = next(res.find(lambda x: x['class'] == 'value'))
            self.ccost = int(res.__fields__['data'].strip('"').strip())

            ## get the expansion
            res = next(tree.find(lambda x:'id' in x and x['id'] == "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentSetSymbol"))
            res = res.__children__[1]
            self.expansion = res.__fields__['data']

            ## get the rarity
            res = next(tree.find(lambda x:'id' in x and x['id'] == "ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow"))
            self.rarity = res.__children__[1].__children__[0]['data']

            ## get the rating
            self.rating = float(
                           next(
                            tree.find(
                             lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_currentRating_textRating'))['data'])

            ## get the MUID
            res = next(tree.find(lambda x:'id' in x and x['id'] == 'ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_cardImage'))
            m = re.findall('multiverseid=([0-9]+)', res.__fields__['src'])
            self.muid = int(m[0])

            ## get the image URL
            ### a constant string and the MUID
            self.img = ("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%i&type=card" % self.muid)

            self.keywords = [ k for k in self.__keywords__ if k.lower() in self.text.lower()]
        except:
            raise RuntimeError("Failed to load deck")
        finally:
            return(tree)



#def test():
#    from .cardtestdata import __test_html__
#    for html in __test_html__:
#        c = Card(None)
#        c.loadFromGatherer(html)
#        for k in c.__fields__:
#            try:
#                print(k, getattr(c, k))
#
#            except Exception as e:
#                print(k, e)
#                continue
#
#        print(c.export())
#    return
#
#test()
#
