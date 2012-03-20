#!/usr/bin/env python2

from pymongo.connection import Connection
import socket
import threading
import pickle
import string
import time
import re

global db
connection = Connection("146.6.213.39")
db = connection.magic


class connectionThread(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.__conn__   = conn
        self.__running__= True
        self.__last__   = 0
        self.__client__ = socket.gethostbyaddr(self.__conn__.getpeername()[0])[0]

    def join(self):
        self.__running__ = False
        self.__conn__.send("DONE".encode())
        print("[ %30s ] Thread killed..." % (self.__client__))
        try:
            threading.Thread.join(self)
        except:
            return

    def run(self):
        global ticker
        data = " "
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


class Server(object):
    __thread__  = None
    __clients__ = []
    __host__    = ''
    __port__    = 0
    __buff__    = 0
    __addr__    = ''
    __up__      = False
    __sock__    = None
    __count__   = 0

    def __init__(self, host='', port=9001, buff=1024):
        self.__host__   = host
        self.__port__   = port
        self.__buff__   = buff
        self.__addr__   = (self.__host__, self.__port__)
        self.__up__     = True

        self.__sock__   = socket.socket()
        self.__sock__.bind(self.__addr__)
        self.__sock__.settimeout(1.0)
        self.__sock__.listen(2)

    def run(self):
        if self.__thread__:
            return
        else:
            self.__thread__ = threading.Thread(target=self.__run__)
            self.__thread__.start()

    def stop(self):
        if self.__thread__:
            for t in self.__clients__:
                t.join()
                print("Killed thread", t)
            self.__up__ = False
            self.__thread__.join()
            print("Thread killed...")

        else:
            print("Server was not running..")

    def __run__(self):
        print("Awaiting connections. . .")
        while self.__up__:
            try:
                client      = self.__sock__.accept()
                print("Client connected from {}.".format(client[1]))

                self.__clients__.append(connectionThread(client[0]))
                self.__clients__[-1].start()

            except socket.timeout:
                continue

if __name__ == "__main__" or 1:
    global ticker, limit
    ticker = 801914
    limit = 920000
    serv = Server()
    serv.run()
    input()
    serv.stop()
