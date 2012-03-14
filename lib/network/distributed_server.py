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
        self.__conn__ = conn
        self.__running__ = True
        self.__last__ = 0
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
            print("[", self.ident, "] SIGNAL FROM", self.__conn__.getpeername())

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

    def handleNewClient(self, client):
        print("Client connected from {}.".format(client[1]))
        c = connectionThread(client[0])
        self.addHandler(c)
        c.start()

    def addHandler(self, handler):
        self.__clients__.append(handler)

    def __run__(self):
        print("Awaiting connections. . .")
        while self.__up__:
            try:
                client = self.__sock__.accept()
                self.handleNewClient(client)

            except socket.timeout:
                continue

if __name__ == "__main__":
    global ticker, limit
    ticker = 801914
    limit = 920000
    serv = Server()
    serv.run()
    input()
    serv.stop()
