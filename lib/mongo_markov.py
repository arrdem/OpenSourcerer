#!/usr/bin/env python

from pymongo.connection import Connection 
import random
import time

class MongoMarkovChain(object):
    __last__        = None
    __db__          = None
    __table__       = None

    def __init__(self, db, table):
        self.__db__ = db
        self.__table__ = table

    def add(self, a, b, value=1):
        pass

    def get(self):
        if self.__last__ == None:
            # pick one at random
            t = self.__db__[self.__table__].find()  # select all the documents
            self.__last__ = t.skip(random.randint(0,t.size()-1))

        else:
            i = random.randint(0, int(self.__last__['sum']))
            s = 0
            for k in self.__last__:
                if k == 'name':
                    continue
                elif k == '_id':
                    continue
                else:
                    s += self.__last__[k]
                if s >= i:
                    self.__last__ = self.__db__[self.__table__].find({'name':k})[0]

        return self.__last__['name']

