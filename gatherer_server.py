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
        self.__verbose__ = False

    def run(self):
        global generator
        data = " "
        connection = Connection("146.6.213.39")
        db = connection.magic

        while self.__running__ and data:
            data = str(self.__conn__.recv(4096), "utf-8")
            if(self.__verbose__): print("[ %40s ] SIGNAL %s" % (self.__client__, data))

            if data == "NEXT":
                ticker = generator.next()
                self.__last__ = ticker
                self.__conn__.send(str("PAGEID %i" % (ticker)).encode())
                if(self.__verbose__): print("[ %40s ] SIGNALING %i" % (self.__client__, ticker))

            elif "FAIL" in data:
                i = int(re.sub("FAIL ", '', data))
                if(self.__verbose__): print("[ %40s ] FAILED TO DOWNLOAD CARD ID %i" % (self.__client__,  i))
                generator.logfail(self.__last__)

            elif "ERROR" in data:
                print("[ %40s ] %s" % (self.__client__, data))

            elif "FATAL" in data:
                print("[ %40s ] NODE DOWN '%s'" % (self.__client__, data))
                self.join()

            elif "OKAY" in data:
                # this is the signal from the client that a new deck has
                # been found. Format is as follows:
                # DECK (bytes)
                # followed by the pickled dict
                try:
                    i = int(data.split(' ',1)[1])
                    self.__conn__.send('GOAHEAD'.encode())
                    if(self.__verbose__): print("[ %40s ] SIGNALING %s" % (self.__client__, "OK"))
                except Exception as e:
                    if(self.__verbose__): print(e)
                    exit(1)

                deck = None
                try:
                    deck = pickle.loads(self.__conn__.recv(i))
                    self.__conn__.send('1'.encode())
                    if(self.__verbose__): print("[ %40s ] SIGNALING %s" % (self.__client__, '1'))
                except:
                    self.__conn__.send('0'.encode())
                    if(self.__verbose__): print("[ %40s ] SIGNALING %s" % (self.__client__, '0'))

                if deck is not None:
                    deck['_id'] = str(self.__last__)
                    db.cards.insert(deck)

                    print("[ %40s ] DOWNLOADED CARD %i : %s" % \
                             (self.__client__, self.__last__, deck['name']))


        if(not data):
            print("[ %40s ] NO TRAFFIC, EXITING" % (self.__client__))


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
        self.__fail_limit__ = 25
        self.__last__ = 0
        self.__gen__ = chain(self.__seed_MIDs__, self.getRandomMUID())

    def __iter__(self):
        return self.__last__

    def logfail(self, i):
        self.__fail_count__ += 1

    def next(self):
        if(self.__last__ == 0):
            self.__last__ = next(self.__gen__)

        elif(self.__fail_count__ < self.__fail_limit__):
            n = self.__last__ + self.__delta__
            if n in self.__used_muids__:
                self.__last__ = next(self.__gen__)
            else:
                self.__last__ = n

        elif(self.__fail_count__ >= self.__fail_limit__) and (not self.__delta__):
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
                elif(c > 100):  # this means at least 99.9% completion.
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
