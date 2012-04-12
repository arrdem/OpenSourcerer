#!/usr/bin/env python
from ..markov.mongo_markov import MongoMarkovChain as mc
from collections import defaultdict as bag
import ..ai.land_ai as  land_ai

class DeckGenerator:
    def __init__(self, db, restrict=None, seed=None):
        self.__restrict__ = restric
        self.__seed__     = seed
        self.__db__       = db
        self.__deck__     = bag(lambda: 0)

    def generate(self, count=60, exp=1.2, table='markov'):
        pass

class MarkovDeckGenerator(DeckGenerator):
    def __init__(self, *args, **kwargs):
        DeckGenerator.__init__(self, *args, **kwargs)

    def generate(self, count=60, exp=1.2, table='markov'):
        self.__deck__     = bag(lambda: 0)

        ai = mc(self.__db__, table, exp=exp)
        for i in range(count):
            a = ai.get()
            self.__deck__[a] += 1

            if a.name not in self.__cards__:
                self.__cards__[name] = a

        return self.__deck__

class NeuralLandMarkov(DeckGenerator):
    def __init__(self, *args, **kwargs):
        DeckGenerator.__init__(self, *args, **kwargs)

    def generate(self, count=60, table='markov', ):
        self.__deck__     = bag(lambda: 0)

        ai = mc(self.__db__, table, exp=exp)

        for i in range(int(count * (2/3))):
            while 1:
                c = ai.get()
                if c not in land_ai.__lands__:
                    self.__deck__[c] += 1
                    break

        v = land_ai.input_vector(self.__deck__, self.__db__)
        net = pickle.load(open(parser.get('land_net', 'brain')))
        ov = net.activate(v)
        for i in range(len(land_ai.__lands__)):
            self.__deck__[land_ai.__lands__[i]] = int(ov[i]*count*0.33333333334)

        return self.__deck__

class RestrictedCardMarkov(DeckGenerator):

