#!/usr/bin/env python2
# This file defines the server side of a distributed gatherer-scraping system

from lib.network.distributed_server import Server
from lib.network.distributed_server import connectionThread
from pymongo.connection import Connection
from ConfigParser import SafeConfigParser
from itertools import chain
import curses
import urllib
import pickle
import time
import re

global parser
parser = SafeConfigParser()
parser.read('settings.ini')

class GathererThread(connectionThread):

    def __init__(self, conn):
        connectionThread.__init__(self, conn)
        self.__verbose__ = False
        self.__count__ = 0
        self.__failures__ = 0
        self.__fail_count__ = 0
        self.__fail_limit__ = 10
        self.__s_time__ = time.time()

        global x, y
        self.__cursor_x__ = x
        self.__cursor_y__ = y
        y += 1

    def _print(self, *args):
        global outpad
        for a in args:
            outpad.addstr(self.__cursor_y__,
                          self.__cursor_x__,
                          " %s" % (str(a),))
        #outpad.border('|', '|')
        outpad.refresh()

    def send(self, string):
        self.__conn__.send(string.decode())

    def status(self):
        self._print(" %30s Errors: %i    Successes: %i    Pageid: %i    Status: %s" %
                    (self.__client__, self.__failures__, self.__count__,
                     self.__last__, str(self.__running__)))

    def run(self):
        global generator
        data = " "
        connection = Connection(parser.get('mongodb', 'server'))
        db = None
        exec('db = connection.' + parser.get('mongodb', 'db'))

        while self.__running__ and data:
            data = str(self.__conn__.recv(1024*32)).decode("utf-8",
                                                            errors='ignore')
            self.status()

            if data == "NEXT":
                ticker = generator.next()
                self.__last__ = ticker
                self.__conn__.send(str("PAGEID %i" % (ticker)).encode())

            elif "FAIL" in data:
                i = int(re.sub("FAIL ", '', data))
                generator.logfail(self.__last__)

            elif "ERROR" in data:
                self._print("%-100s" % (" %30s %s" % (self.__client__, data)))

            elif "FATAL" in data:
                self._print("%-100s" % (" %30s NODE DOWN '%s'" % (self.__client__, data)))
                self.join()

            elif "OKAY" in data:
                if(self.__fail_count__ < self.__fail_limit__):
                    try:
                        i = int(data.split(' ',1)[1])
                        self.__conn__.send('GOAHEAD'.encode())
                    except Exception as e:
                        exit(1)

                    card = None
                    try:
                        card = pickle.loads(self.__conn__.recv(i))
                        self.__fail_count__ = 0
                        self.__conn__.send('1'.encode())
                        self.__count__ += 1
                    except Exception as e:
                        self.__fail_count__ += 1
                        self.__conn__.send('0'.encode())

                    if card is not None:
                        card['_id'] = str(self.__last__)
                        db.cards.insert(card)

                        self._print("%-100s" % (" %30s DOWNLOADED CARD %i : %s" % \
                                (self.__client__, self.__last__, card['name'])))
                else:
                    self.__conn__.send('1'.encode())
                    self.__fail_count__ = 0
                    self.__failures__ += 1
                    self._print("%-100s" % (" %30s FAILES TO DOWNLOADED CARD %i" % \
                                 (self.__client__, self.__last__)))

        if(not data):
            self._print("%-100s" % (" %30s NO TRAFFIC, EXITING" % (self.__client__)))
            self.join()


class GathererServer(Server):

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def handleNewClient(self, client):
        global clients
        #print "Client connected from {}.".format(client[1])
        handler = GathererThread(client[0])
        clients[handler.__client__] = handler
        self.addHandler(handler)
        handler.start()

class MUIDItterator():
    __seed_MIDs__= list(map(int, parser.get('scrape', 'seeds').split(',')))

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

    stdscr = curses.initscr()
    curses.echo()
    curses.cbreak()
    curses.setsyx(150, 1)

    global outpad
    outpad = curses.newwin(115, 100, 0, 0)
    inpad = curses.newwin(40, 50, 0, 101)

    inpad.scrollok(True)
    inpad.idlok(True)

    outpad.scrollok(True)
    outpad.idlok(True)

    global x, y
    x, y = 1, 1

    serv = GathererServer()
    serv.run()

    global clients
    clients = {}

    inpad.addstr('\n')
    while 1:
        inpad.addstr(' $ ')
        inpad.border('|', '|')
        inpad.refresh()
        cmd = str(inpad.getstr()).decode('utf-8', errors='ignore').split(' ', 1)

        if cmd[0] == 'send':
            conn.send(cmd[1].encode())

        elif cmd[0] == 'exit':
            serv.stop()
            curses.endwin()
            break

        else:
            try:
                exec(' '.join(cmd))
            except Exception as e:
                print(e)
