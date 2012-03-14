#!/usr/bin/env python3
# This file defines the server side of a distributed gatherer-scraping system

from lib.network.distributed_server import Server
from lib.network.distributed_server import connectionThread
from pymongo.connection import Connection
from bson.objectid import ObjectId
from itertools import chain
import urllib.request as urllib
import pickle
import string
import time
import re


class GathererThread(connectionThread):

    def __init__(self, conn):
        connectionThread.__init__(self, conn)

    def run(self):
        global generator
        data = " "
        connection = Connection("146.6.213.39")
        db = connection.magic

        while self.__running__ and data:
            data = str(self.__conn__.recv(4096), "utf-8")
            print("[", self.ident, "] SIGNAL FROM",
                  self.__client__, data)

            if data == "NEXT":
                ticker = generator.next()
                self.__last__ = ticker
                self.__conn__.send(str(ticker).encode())

            elif "FAIL" in data:
                i = int(re.sub("FAIL ", '', data))
                #print("[ %30s ] FAILED TO DOWNLOAD DECK ID %i" % (self.__client__,  i))
                generator.logfail(self.__last__)

            elif "OKAY" in data:
                # this is the signal from the client that a new deck has
                # been found. Format is as follows:
                # DECK (bytes)
                # followed by the pickled dict
                try:
                    i = int(re.sub("OKAY ", '', data))
                    self.__conn__.send('OK'.encode())
                except:
                    continue

                deck = None
                try:
                    deck = pickle.loads(self.__conn__.recv(i))
                    self.__conn__.send('1'.encode())
                except:
                    self.__conn__.send('0'.encode())

                if deck is not None:
                    deck['_id'] = ObjectId()
                    db.cards.insert(deck)

                    print("[ %30s ] DOWNLOADED DECK %i" % \
                             (self.__client__, self.__last__))

        if(not data):
            print("[ %30s ] NO TRAFFIC, EXITING" % (self.__client__))


class GathererServer(Server):

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def handleNewClient(self, client):
        print("Client connected from {}.".format(client[1]))
        handler = GathererThread(client[0])
        self.addHandler(handler)
        handler.start()

class MUIDItterator():
    __seed_MIDs__= [
        108933,191306,80530,45374,191056,39675,19891,2729,1229,178113,97052,
        198386,87913,220955,100,4807,1923,37909,1239,89019,96936,3371,126294,
        193511,182270,1665,116747,6550,3315,20225,4851,96873,189272,140183,
        226589,247358,206343,194208,213792,243464,242485,244335,244332,244330,
        244325,244320]

    def __init__(self):
        self.__used_muids__ = set()
        self.__last_muid__ = None
        self.__last_random_muid__ = None
        self.__delta__ = -1
        self.__fail_count__ = 0
        self.__last__ = 0
        self.__gen__ = chain(self.__seed_MIDs__, self.getRandomMUID())

    def __iter__(self):
        return self.__last__

    def logfail(self, i):
        self.__fail_count__ += 1

    def next(self):
        if(self.__last__ == 0):
            self.__last__ = next(self.__gen__)

        elif(self.__fail_count__ < 50):
            self.__last__ = self.__last__ + self.__delta__

        elif(self.__fail_count__ >= 50) and (not self.__delta__):
            self.__fail_count__ = 0
            self.__last__ = self.__last_muid__ + 1
            self.__delta__ = 1

        else:
            self.__fail_count__ = 0
            self.__last__ = next(self.__gen__)
        self.__used_muids__.add(self.__last__)
        return self.__last__


    def getRandomMUID(self):
        opener = urllib.build_opener(urllib.HTTPErrorProcessor(),
                                     urllib.HTTPRedirectHandler(),
                                     urllib.HTTPHandler())
        request = urllib.Request("http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random")
        c = 0
        while 1:
            try:
                response = opener.open(request)
            except Exception as e:
                i = int(e.__dict__['url'].split('=')[1])
                if i not in self.__used_muids__:
                    yield i
                elif(c > 100):
                    raise StopIteration()
                else:
                    c += 1


if __name__ == "__main__":
    global generator
    generator = MUIDItterator()
    serv = GathererServer()
    serv.run()
    input()
    serv.stop()
