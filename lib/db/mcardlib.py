#!/usr/bin/env python
#
#   Copyright Reid McKenzie, 2011
#
#   The CARD data structure (V2, a dict)
#       ["Multiverse ID:"]              TYPE: int
#       ["Card Name:"]                  TYPE: str
#       ["Types:"]                      TYPE: list
#           FORMAT: list of single word strings
#
#       ["TAGS"]                        TYPE: list
#           FORMAT: see TYPE
#       ["Card Text:"]                  TYPE: str
#       ["Mana Cost:"]                  TYPE: list
#           FORMAT: list of ints
#                   [RED, BLUE, BLACK, GREEN, WHITE, ANY, TOTAL]
#
#       ["P/T:"]                        TYPE: list
#           FORMAT: (CREATURE MUST BE IN TYPEs) [INT, INT]
#
#       ["Loyalty:"]                    TYPE: int
#       ["Artist:"]                     TYPE: str
#       ["Rarity:"]                     TYPE: str
#       ["Community Rating:"]           TYPE: float

_Format = { "Card Name:"           :       type(str),
            "Mana Cost:"           :       type(list),
            "Converted Mana Cost:" :       type(int),
            "Types:"               :       type(list),
            "Card Text:"           :       type(str),
            "Flavor Text:"         :       type(str),
            "P/T:"                 :       type(list),
            "Expansion:"           :       type(str),
            "Rarity:"              :       type(str),
            "Artist:"              :       type(str),
            "Community Rating:"    :       type(str),
            "Hand/Life:"           :       type(list),
            "Loyalty:"             :       type(int),
            "Multiverse ID:"       :       type(int),
            "Community Rating:"    :       type(float),
            "Community Votes:"     :       type(int),
            "Meta Rating:"         :       type(int),
            "Img File:"            :       type(str),
            "Img MD5Sum:"          :       type(str)
            }

_Keys = [   "Card Name:",
            "Mana Cost:",
            "Converted Mana Cost:",
            "Types:",
            "Card Text:",
            "Flavor Text:",
            "P/T:",
            "Expansion:",
            "Rarity:",
            "Artist:",
            "Community Rating:",
            "Hand/Life:",
            "Loyalty:",
            "Multiverse ID:",
            "Community Rating:",
            "Community Votes:",
            "Meta Rating:",
            "Img File:",
            "Img MD5Sum:"
        ]

_keywords = ["Absorb","Affinity","Amplify","Annihilator","Attach",
"Aura swap","Banding","Bands with other","Bloodthirst","Bury","Bushido",
"Buyback","Cascade","Champion","Changeling","Channel","Chroma","Clash",
"Conspire","Convoke","Counter","Cumulative Upkeep","Cycling",
"Deathtouch","Defender","Delve","Devour","Domain","Double strike",
"Dredge","Echo","Enchant","Entwine","Epic","Equip","Evoke","Exalted",
"Exile","Fading","Fateseal","Fear","First strike","Flanking","Flash",
"Flashback","Flying","Forecast","Fortify","Frenzy","Graft","Grandeur",
"Gravestorm","Haste","Haunt","Hellbent","Hexproof","Hideaway",
"Horsemanship","Imprint","Infect","Intimidate","Join forces","Kicker",
"Kinship","Landfall","Swampwalk","Islandwalk","Mountainwalk",
"Forestwalk","Planeswalk","Landwalk","Swamphome","Islandhome",
"Mountainhome","Foresthome","Planeshome","Landhome","Level up",
"Lifelink","Madness","Metalcraft","Modular","Morph","Multikicker",
"Ninjuts","Offering","Persist","Phasing","Poisonous","Protection",
"Provoke","Prowl","Radiance","Rampage","Reach","Rebound","Recover",
"Regenerate","Reinforce","Replicate","Retrace","Ripple","Sacrifice",
"Scry","Shadow","Shroud","Soulshift","Splice","Split second","Storm",
"Substance","Sunburst","Suspend","Sweep","Tap","Threshold","Kicker",
"Trample","Transfigure","Transmute","Totem armor","Unearth","Untap",
"Vanishing","Vigilance","Wither"]

Any = (True, False, None)

def RE(line):
    try:
        return eval(line)
    except Exception:
        return []

def load(file = "./cards.dat"):
    """returns a list of card formatted lists """
    file = open(file)
    t = [RE(line) for line in file if len(line)>1]
    return [i for i in t if len(i)>0]

def write(data, file = "./cards.dat", mode = "w"):
    """a card data writer which takes an itterable as the argument.
 designed for lists of cards."""
    for foo in data:
        writeln(foo, file = file, mode = mode)

def writeln(data, file = "./cards.dat", mode = "a"):
    """a card data writer which takes a single line"s worth of data as the argument."""
    open(file, mode).write(repr(data)+"\n")

def _f(card, index, target):
    r = []
    for i in range(len(target)):
        if target[i] == Any:
            r+=[True]
        else:
            r += [card[index][i] == target[i]]
    return not (False in r)

def search(data, index, target):
    """a simple tool for searching the lists returned by load()"""
    # here data is a list of the same format returned by load().
    # search returns every instance of a card which matches the input
    # description. NOTE - None is a wildcard
    if type(target) == type([]) and  Any in target:
        return [card for card in data if _f(card, index, target)]
    else:
        return [card for card in data if card[index] == target]

def find(data, target):
    """a tool for matching multiple values in a card."""
    # the format of target is the same as a standard line.
    # probably worthless... need to rethink searching.

    keys = [i for i in range(len(target)) if target[i]]

    for foo in keys:
        data = search(data, foo, target[foo])

    return data

def getMUID(url = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"):
    import re, urllib2
    data = "".join(urllib2.urlopen(url).readlines())
    data = re.compile("""multiverseid=[0-9]*?\"""").search(data).group(0)
    data = re.sub(re.compile("""\D"""),"",data)
    return int(data)
