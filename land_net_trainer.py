#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
import pickle

__land_format__ = ['Black', 'Blue', 'Green', 'Red', 'White', '*']
__lands__ = ['Island', 'Swamp', 'Mountain', 'Plains', 'Forrest']

def input_vector(deck, db):

    iv = [0] * 19
    cards = {card: db.findOne({'name': card}) for card in deck}

    cost_types = ['Black', 'Blue', 'Green', 'Red', 'White', '*']

    cost_list = [[card['cost'][type] for card in deck
                        if type in card['cost']]
                for type in cost_types]

    sum_costs = [sum(c) for c in cost_list]
    avg_costs = [sum(c) / len(c) for c in cost_list]
    percentage_costs = [c / deck['sum'] for c in sum_costs]
    most_expensive = sorted([cards[c] for c in cards],
                            key=lambda card: sum([card['cost'][t]
                                                for t in card['cost']]),
                            reverse=True)[0]

    return map(float, ([most_expensive['cost'][k]
                        for k in cost_types if k in most_expensive['cost']] +
                       avg_costs + percentage_costs +
                       [deck['sum'] - sum([deck[land] for land in
                                           __lands__ if land in deck])]))


def output_vector(deck):
    res = []
    for land in __lands__:
        if land in deck:
            res.append(float(deck[land]))
        else:
            res.append(0.0)
    return res

if __name__ == '__main__':
    # Land Filler Network Spec
    #   Inputs (conceptual):
    #       Most expensive card, Average cc, percentage split by color,
    #       deck size without lands
    #   Inputs (practical):
    #       6*float for the most expensive card
    #       6*float for the average cc
    #       6*float for percentage split by color
    #       1*float for card count sans lands
    #   Total: 19 inputs
    #
    #   Outputs:
    #       6*float, one per card type (count of reccomended)

    net = buildNetwork(19,         #INPUT NODES
                       14,         #HIDDEN NODES
                       6           #OUTPUTS
                      )
    ds = SupervisedDataSet(19,     #INPUT VECTOR SIZE
                           6       #OUTPUT VECTOR SIZE
                          )

    connection = Connection("146.6.213.39")
    db = connection.magic
    cursor = db.decks.find().limit(800)

    for deck in cursor:
        ds.addSample(tuple(input_vector(deck)), tuple(output_vector(deck)))

    trainer = BackpropTrainer(net, ds)
    trainer.train()

    while 1:
        cmd = raw_input(">>> ")
        cmd = cmd.split(' ',1)

        if cmd[0] == 'fill':
            try:
                deck = exec(cmd[1])
                print(net.activate(input_vector(deck)))
            except:
                pass

        if cmd[0] == 'exit':
            exit(0)

        if cmd[0] == 'save':
            f = open(cmd[1],'wb')
            pickle.dump(net, f)
