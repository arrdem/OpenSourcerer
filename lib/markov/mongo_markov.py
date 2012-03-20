#!/usr/bin/env python

from pymongo.connection import Connection
from .markov import MarkovChain as Markov
import random
import time

class MongoMarkovChain(Markov):
    __last__        = None
    __db__          = None
    __table__       = None

    def __init__(self, db, table):
        Markov.__init__(self)
        self.__db__ = db
        self.__table__ = table

    def add(self, a, b, value=1):
        pass

    def get(self):
        if self.__last__ == None:
            # pick one at random
            t = self.__db__[self.__table__].find()  # select all the documents
            self.__last__ = t.skip(random.randint(0,t.count()-1))[0]
            return self.__last__

        else:
            previous = self.__last__
            i = random.randint(0, int(self.__last__['sum']))
            s = 0
            for k in self.__last__:
                if k in ['name', '_id', 'sum']:
                    continue
                else:
                    try:
                        if k in self.__last__:
                            s += self.__last__[k]
                    except:
#                        print(repr(k), type(k), "  -  ", self.__last__[k], type(self.__last__[k]))
                        self.__db__[self.__table__].update({'_id': self.__last__['_id']},
                                                           { "$unset" : { k : 1} })
                        self.__db__[self.__table__].remove({'name': k})
                        continue

                if(s >= i) and not isinstance(self.__last__['name'], dict):
 #                   print(s, i)
                    self.__last__ = self.__db__[self.__table__].find({'name':k}).limit(1)[0]
                    break

        if(self.__last__ == previous):
            return self.get()

        return self.__last__['name']
