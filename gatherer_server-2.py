#!/usr/bin/env python2
# This file defines the server side of a distributed gatherer-scraping system

from lib.network.distributed_server import Server
from lib.network.distributed_server import connectionThread
from pymongo.connection import Connection
from ConfigParser import SafeConfigParser
from itertools import chain
import mechanize
import curses
import json
import time
import sys
import re


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
        self.__cursor_x__ = int(x)
        self.__cursor_y__ = int(y)
        y += 1

    def _print(self, *args):
        global outpad
        try:
            outpad.addstr(self.__cursor_y__,
                          self.__cursor_x__,
                          ' '.join(map(str, args)))
            refresh()
        except:
            pass

    def join(self):
        global __active_hosts__
        __active_hosts__ -= 1
        self.__running__ = False
        connectionThread.join(self)

    def send(self, string):
        self.__conn__.send(string.decode())

    def status(self):
        self._print("%-100s" % (" %35s E: %3i    S: %8i    P: %8i    S: %s" %
                    (self.__client__, self.__failures__, self.__count__,
                     self.__last__, str(self.__running__))))

    def run(self):
        global generator
        data = " "
        connection = Connection(parser.get('mongodb', 'server'))
        db = None
        exec("db = connection." + parser.get('mongodb', 'db'))

        while self.__running__ and data:
            data = str(self.__conn__.recv(1024 * 32)).decode("utf-8",
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
                self._print("%-100s" % (" %35s %s" % (self.__client__, data)))

            elif "FATAL" in data:
                self._print("%-100s" %
                            (" %35s NODE DOWN '%s'" % (self.__client__, data)))
                self.join()

            elif "OKAY" in data:
                if(self.__fail_count__ < self.__fail_limit__):
                    try:
                        i = int(data.split(' ', 1)[1])
                        self.__conn__.send('GOAHEAD'.encode())
                    except Exception:
                        exit(1)

                    card = None
                    try:
                        card = json.loads(self.__conn__.recv(i))
                        self.__fail_count__ = 0
                        self.__conn__.send('1'.encode())
                        self.__count__ += 1
                    except Exception:
                        self.__fail_count__ += 1
                        self.__conn__.send('0'.encode())

                    if card is not None:
                        card['_id'] = str(self.__last__)

                        db.cards.insert(card)

                        global __card_count__
                        __card_count__ += 1

                        self._print("%-100s" %
                            (" %35s DOWNLOADED CARD %8i : %s" % \
                                (self.__client__, self.__last__, card['name'])))

                else:
                    self.__conn__.send('1'.encode())
                    self.__fail_count__ = 0
                    self.__failures__ += 1
                    self._print("%-100s" %
                            (" %35s FAILED TO DOWNLOADED CARD %8i" % \
                                 (self.__client__, self.__last__)))

        if(not data):
            self._print("%-100s" %
                            (" %35s NO TRAFFIC, EXITING" %
                                (self.__client__)))
            self.join()


class GathererServer(Server):
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def handleNewClient(self, client):
        global clients, __active_hosts__
        #print "Client connected from {}.".format(client[1])
        handler = GathererThread(client[0])
        handler.daemon = False
        clients[handler.__client__] = handler
        self.addHandler(handler)
        handler.start()
        __active_hosts__ += 1


class MUIDItterator():
    def __init__(self):
        global parser
        self.__seed_MIDs__ = list(
                              map(int,
                                  parser.get('gatherer', 'seeds').split(',')))

        self.__used_muids__ = set()
        self.__last_muid__ = None
        self.__last_random_muid__ = None
        self.__delta__ = -1
        self.__fail_count__ = 0
        self.__fail_limit__ = 25
        self.__limit__ = 1000
        self.__last__ = 0
        self.__gen__ = chain(self.__seed_MIDs__, self.getRandomMUID())
        self.__browser__ = mechanize.Browser()
        self.__browser__.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

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

        elif((self.__fail_count__ >= self.__fail_limit__) and
             (not self.__delta__)):
            self.__fail_count__ = 0
            self.__last__ = self.__last_muid__ + 1
            self.__delta__ = 1

        else:
            self.__fail_count__ = 0
            self.__last__ = next(self.__gen__)

        self.__used_muids__.add(self.__last__)
        return self.__last__

    def getRandomMUID(self):
        c = 0
        while 1:
            self.__browser__.open("http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random")
            s = self.__browser__.geturl()
            i = int(s.split('=', 1)[1])
            #print "GOT INDEX", i
            if i not in self.__used_muids__:
                yield i
            elif(c > self.__limit__):  # this means at least 99.9% completion.
                raise StopIteration()
            else:
                c += 1


def refresh():
    global outpad, inpad
    for pad in [inpad, outpad]:
        pad.refresh()
    curses.doupdate()


def pprint(pad, *args):
    global __linecount__
    if(__linecount__ > 39):
        pad.addstr(0, 0, ' ' * (max_x - 100) + '\n' * 40)
        pad.addstr(0, 0, '')
        __linecount__ = 0

    for a in args:
        pad.addstr(" %s" % (str(a),))
    pad.addstr('\n')
    refresh()
    __linecount__ += 1


if __name__ == "__main__":
    sys.stderr = open('/dev/null', 'w')

    global __linecount__, __card_count__, __active_hosts__
    __linecount__ = 0
    __card_count__ = 0
    __active_hosts__ = 0

    global parser
    parser = SafeConfigParser()
    parser.read('settings.ini')

    global generator
    generator = MUIDItterator()

    stdscr = curses.initscr()
    curses.echo()
    curses.cbreak()
    curses.setsyx(150, 1)

    global outpad, max_y, max_x
    max_y, max_x = stdscr.getmaxyx()
    print  max_x, max_y
    outpad = curses.newwin(max_y, 100, 0, 0)
    inpad = curses.newwin(500, max_x - 100, 0, 101)

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
        try:
            inpad.addstr(' $ ')
            inpad.refresh()
            cmd = str(inpad.getstr()).decode('utf-8',
                                             errors='ignore').split(' ')

            if cmd[0] == 'send':
                if cmd[1] in clients:
                    clients[cmd[1]].send(' '.join(cmd[1::]))
                else:
                    pprint(inpad, 'NO SUCH HOST')

            elif cmd[0] == 'stop':
                if len(cmd) > 1:
                    if cmd[1] in clients:
                        clients[cmd[1]].join()

                    elif cmd[1] == 'all':
                        for c in clients:
                            clients[c].join()

                    else:
                        pprint(inpad, 'NO SUCH HOST')

            elif cmd[0] == 'upgrade':
                for c in clients:
                    clients[c].send('RECONNECT %s' %
                                     (cmd[1] if len(cmd) > 1 else '60'))
                pprint(inpad, ' ready to upgrade...')
                serv.stop()
                curses.endwin()
                sys.exit(0)
                break

            elif cmd[0] == 'list':
                for h in clients:
                    pprint(inpad, h)

            elif cmd[0] == 'exit':
                serv.stop()
                curses.endwin()
                exit(0)
                break

            elif cmd[0] == 'refresh':
                refresh()

            elif cmd[0] == 'count':
                if cmd[1] == 'hosts':
                    pprint(inpad, str(len(clients)))
                elif cmd[1] == 'cards':
                    pprint(inpad, str(__card_count__))
                elif cmd[1] == 'active':
                    pprint(inpad, str(__active_hosts__))
                else:
                    pprint(inpad, "sorry, don't know how to count that.")

            elif cmd[0] == 'clear':
                if cmd[1] == 'input':
                    inpad.erase()
                elif cmd[1] == 'output':
                    outpad.erase()
                else:
                    pprint(inpad, "sorry, don't know how to clear that buffer.")
                refresh()

            else:
                try:
                    exec(' '.join(cmd))
                except Exception as e:
                    pprint(inpad, e)

        except Exception as e:
            pprint(inpad, str(e))
