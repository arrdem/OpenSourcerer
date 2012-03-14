#!/usr/bin/env python2

from lib.network.distributed_server import Server
from lib.network.distributed_server import connectionThread

from pymongo.connection import Connection
import pickle
import string
import time
import re

class EssentialMagicThread(connectionThread):

    def __init__(self, conn):
        connectionThread.__init__(self)

    def run(self):
        global ticker
        data = " "
        connection = Connection("146.6.213.39")
        db = connection.magic

        while self.__running__ and data:
            data = str(self.__conn__.recv(4096), "utf-8")
            #print("[", self.ident, "] UPKEEP SIGNAL FROM", self.__conn__.getpeername())

            if(ticker >= limit):
                self.__conn__.send(str("DONE").encode())
                self.join()

            elif data == "NEXT":
                ticker += 1
                self.__last__ = ticker
                self.__conn__.send(str(ticker).encode())

            elif "FAIL" in data:
                i = int(re.sub("FAIL ", '', data))
                #print("[ %30s ] FAILED TO DOWNLOAD DECK ID %i" % (self.__client__,  i))

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
                    m = {}
                    for c in deck:
                        m[c] = deck[c]

                    m['sum'] = len(deck)

                    for c1 in deck:
                        db.markov.update({'name': c1}, {"$inc": m}, upsert=True)

                    print("[ %30s ] DOWNLOADED DECK %i" % \
                             (self.__client__, self.__last__))

        if(not data):
            print("[ %30s ] NO TRAFFIC, EXITING" % (self.__client__))


class EssentialMagicServer(Server):
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def handleNewClient(self, client):
        print("Client connected from {}.".format(client[1]))
        handler = EssentialMagicThread(client[0])
        self.addHandler(handler)
        handler.start()

if __name__ == "__main__":
    global ticker, limit
    ticker = 801914
    limit = 920000
    serv = EssentialMagicServer()
    serv.run()
    input()
    serv.stop()
