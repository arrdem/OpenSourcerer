#!/usr/bin/env python
# -*- coding: utf-8 *-*
try:
    import numpypy # for PyPy support
except ImportError:
    pass
from numpy import array

__lands__ = ['Island', 'Swamp', 'Mountain', 'Plains', 'Forest']
__cost_types__ = ['Blue', 'Black', 'Red', 'White', 'Green']


def pr(*args):
    print args
    return args


def print_output_vector(v):
    for i in range(len(__lands__)):
        print __lands__[i], v[i]


def card_to_cost_vector(card):
    return [(card['cost'][t] if t in card['cost'] else 0)
            for t in __cost_types__]


def input_vector(deck, db):

    cards = {}
    for card in deck:
        cursor = db.cards.find({'name': card}).limit(1)
        if(cursor.count()):
            cards[card] = cursor[0]

    cost_map = {}
    for card in deck:
        if card in cards:
            cost_map[card] = card_to_cost_vector(cards[card])

    nonland_card_count = deck['sum'] - \
            sum([deck[__lands__[i]]
                    for i in range(len(__lands__)) if __lands__[i] in deck])

#    land_count = output_vector(deck)

    sum_costs = [sum([cost_map[card][i] for card in cost_map])
                for i in range(len(__cost_types__))]

#    avg_costs = [sum((cost_map[c][i] for c in cost_map))
#                 for i in range(len(__cost_types__))]
#
    percentage_costs = [float(c) / float(nonland_card_count)
                        for c in sum_costs]

#    most_expensive = sorted([cards[c] for c in cards],
#                            key=lambda card: sum(card_to_cost_vector(card)),
#                            reverse=True)[0]
#
    return list(map(float, percentage_costs))
#   card_to_cost_vector(most_expensive) + avg_costs +  + [nonland_card_count]))


def output_vector(deck):
    a = array([0.0] * 5)
    for i in range(5):
        if __lands__[i] in deck:
            a[i] = float(deck[__lands__[i]])
        else:
            a[i] = 0.0
    return [e / sum(a) for e in a]


def export_vector(v):
    return ' '.join(map(str, v))


def import_vector(s):
    return tuple(map(float, s.split(' ')))
