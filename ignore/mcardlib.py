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
#       ['TAGS']                        TYPE: list
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

_Format = { u"Card Name:"           :       type(unicode),
            u"Mana Cost:"           :       type(list),
            u"Converted Mana Cost:" :       type(int),
            u"Types:"               :       type(list),
            u"Card Text:"           :       type(unicode),
            u"Flavor Text:"         :       type(unicode),
            u"P/T:"                 :       type(list), 
            u"Expansion:"           :       type(unicode),
            u"Rarity:"              :       type(unicode),
            u"Artist:"              :       type(unicode),
            u"Community Rating:"    :       type(unicode),
            u"Hand/Life:"           :       type(list),
            u"Loyalty:"             :       type(int),
            u"Multiverse ID:"       :       type(int),
            u'Community Rating:'    :       type(float),
            u'Community Votes:'     :       type(int),
            u'Meta Rating:'         :       type(int),
            u"Img File:"            :       type(unicode),   
            u"Img MD5Sum:"          :       type(unicode)
            }

_Keys = [   u"Card Name:",
            u"Mana Cost:",
            u"Converted Mana Cost:",
            u"Types:",
            u"Card Text:",
            u"Flavor Text:",
            u"P/T:",
            u"Expansion:",
            u"Rarity:",
            u"Artist:",
            u"Community Rating:",
            u"Hand/Life:",
            u"Loyalty:",
            u"Multiverse ID:",
            u'Community Rating:',
            u'Community Votes:',
            u'Meta Rating:',
            u"Img File:",
            u"Img MD5Sum:"
        ]

_keywords = ['Absorb','Affinity','Amplify','Annihilator','Attach',
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

Any = (True, False, None)

def intersect(a, b):
    """return the intersection of two lists"""
    return list(set(a) & set(b))

def union(a, b):
    """return the union of two lists"""
    return list(set(a) | set(b))

def read(line):
    try:
        return eval(line)
    except Exception:
        return []

def load(file = "./cards.dat"):
    """returns a list of card formatted lists """
    file = open(file)
    t = [read(line) for line in file if len(line)>1]
    return [i for i in t if len(i)>0]

def write(data, file = "./cards.dat", mode = 'w'):
    """a card data writer which takes an itterable as the argument.
 designed for lists of cards."""
    for foo in data:
        writeln(foo, file = file, mode = mode)

def writeln(data, file = "./cards.dat", mode = 'a'):
    """a card data writer which takes a single line's worth of data as the argument."""
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

def getMID(url = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"):
    import re, urllib2
    data = u''.join(urllib2.urlopen(url).readlines())
    data = re.compile("""multiverseid=[0-9]*?\"""").search(data).group(0)
    data = re.sub(re.compile("""\D"""),"",data)
    return int(data)
