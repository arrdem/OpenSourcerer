#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from ConfigParser                     import SafeConfigParser
import McKenzieLib.learning.neuralnet as netlib
import lib.ai.land_ai as ai
import pickle
import sys

__lands__      = ['Island', 'Swamp', 'Mountain', 'Plains', 'Forest']
__cost_types__ = ['Blue', 'Black', 'Red', 'White', 'Green']

def main():
    # Land Filler Network Spec
    #   Inputs (conceptual):
    #       Most expensive card, Average cc, percentage split by color,
    #       deck size without lands
    #   Order
    #       'Blue', 'Black', 'Red', 'White', 'Green'
    #   Inputs (practical):
    #       5*float for the most expensive card    //OLD
    #       5*float for the average cc
    #       5*float for percentage split by color
    #       1*float for card count sans lands
    #   Total: 16 inputs
    #
    #   Outputs:
    #       5*float, one per card type (count of reccomended)

    parser = SafeConfigParser()
    parser.read('settings.ini')

    ds = []

    for l in open(parser.get('land_net', 'corpus')):
        try:
            i, o = map(ai.import_vector, l.split('|'))
            if i and o:
                print i, o
                ds.append((i, o,))
        except:
            pass

    net = None

    if '-l' in sys.argv:
        net = pickle.load(open(parser.get('land_net', 'brain')))
    else:
        net = netlib.NN(int(parser.get('land_net', 'insize')),
                               int(parser.get('land_net', 'hidden')),
                               int(parser.get('land_net', 'outsize')))

    print "CREATED NET WITH DIMENSIONS %i %i %i" % (net.ni, net.nh, net.no)

    print "STARTING TRAINING....."
    net.train(ds, iterations=int(parser.get('land_net', 'iterations')))

    f = open(parser.get('land_net', 'brain'),'wb')

    pickle.dump(net, f, 2)

if __name__ == '__main__':
    main()
