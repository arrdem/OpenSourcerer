#!/usr/bin/env python

import random
import time

class __MarkovNode__():
    __map__ = {}
    __sum__ = 0

    def __init__(self):
        pass

    def add(self, key, value=1):
        if key in self.__map__:
            self.__map__[key] = value + self.__map__[key]
        else:
            self.__map__[key] = value

    def get(self):
        self.__sum__ = sum([self.__map__[k] for k in self.__map__])
        i = random.randint(0, self.__sum__)
        #print "[RANDINT]", i, self.__sum__
        s = 0
        for k in self.__map__:
            s += self.__map__[k]
            if(s >= i):
                return k
            else:
                #print "[NODE.GET] SKIPPING", k
                pass

    def __str__(self):
        return repr(self.__map__)

class MarkovChain(object):
    __last__        = None
    __map__         = {}

    def __init__(self):
        pass

    def add(self, a, b, value=1):
        if a not in self.__map__:
            self.__map__[a] = __MarkovNode__()

        self.__map__[a].add(b, value=value)

    def get(self):
        if self.__last__ == None:
            self.__last__ = self.__map__[random.choice(self.__map__.keys())].get()

        else:
            self.__last__ = self.__map__[self.__last__].get()

        return self.__last__

    def __str__(self):
        return "{" + ', \n'.join([repr(x)+":"+str(self.__map__[x]) for x in self.__map__]) + "}"

    def save(self, f):
        f.write(self.__str__())

    def load(self, f):
        eval("tmpdict = "+''.join(f.readlines()))
        self.__map__ = {}

        for k in tmpdict:
            self.__map__[k] = __MarkovNode__()
            self.__map__[k].__map__ = tmpdict[k]

