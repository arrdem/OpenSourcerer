#!/usr/bin/env python3
# -*- coding: utf-8 *-*
from lib.network.distributed_server import Server, connectionThread

from pymongo.connection import Connection
from configparser import SafeConfigParser
import threading
import socket
import json
import time


class ListenerThread(threading.Thread):
    """
    A simple listener for a message-based server thread which listens on a
    socket and pushes the resulting data onto the parent's stack. This adds an
    extra level of asyncronous interaction to the system and should improve
    performance certainly in signaling from the user to each thread because
    there is a standard and integrated way for the threads to interact with the
    user after the run has been launched.
    """

    def __init__(self, socket, queue):
        super(ListenerThread, self).__init__()
        self.__soc__ = socket
        self.__queue__ = queue
        self.__running__ = True

    def run(self):
        while self.__running__:
            try:
                msg = socket.recv()
                self.__queue__.append(str(msg, 'utf-8', 'ignore'))
            except socket.timeout:
                continue

    def join(self):
        self.__running__ = False
        super(ListenerThread, self).join()


class TournamentThread(connectionThread):
    """
    This class is a handler thread which deals with a single client personally.
    It uses a message queue and a listener thread to maintain asyncronous
    interaction both with the spawning code (to which it is still beholden via
    the message stack) and to its remote client.

    The listener is implemented above.

    An important archetecture point is that __everything__ about this system
    is supposed to be as stateless as possible in order to ensure maximum
    responsiveness and reliabity/verifiability of client and server interaction.
    """
    def __init__(self, *args, **kwargs):
        connectionThread.__init__(self, *args, **kwargs)
        self.__a__ = None    # ID number of deck A
        self.__b__ = None    # ID number of deck B

        self.__queue__ = []
        self.__listener__ = ListenerThread(self.__conn__, self.__queue__)

        global population
        self.population = population

    def __logwin__(self, id):
        """
        Used to record which deck won the series
        """
        if(id == 0):
            self.population.logGame(self.__a__, self.__b__)
        elif(id == 1):
            self.population.logGame(self.__b__, self.__a__)
        else:
            raise Exception("Unexpexted value in __logwin__: %i" % (id))

    def __next__(self):
        """
        Used to generate and send the next pair of decks to the client.
        """
        pass

    def run(self):
        self.__listener__.start()
        while self.__running__:
            if(self.__queue__):
                self.handle(self.__queue__.pop())
            else:
                time.sleep(1)

    def handle(self, data):
        """
        Basically just a big switch/case on the first word of the data which
        determines how the process deals with the data
        """
        data = data.split(' ', 1)
        head, tail = data[0], data[1]

        # first those signals which the client can send
        if(head == 'ERROR'):
            # the client reports a failure...
            print("[ %30s ] Error Reported: '%s'" %
                    (self.__client__, tail))

        elif(head == 'NEXT'):
            # the client requests a new pair of decks
            self.__a__, self.__b__ = next(self.population)

        elif(head == 'RESULTS'):
            # the client has results regarding two decks


        elif(head == 'GET'):
            # the client needs the data which comprises a deck
            which = int(tail)
            if(which == 1):
                self.__conn__.send(
                    json.dumps(
                        self.population.get(
                            self.__a__)).encode())

            if(which == 2):
                self.__conn__.send(
                    json.dumps(
                        self.population.get(
                            self.__b__)).encode())
            else:
                pass

        # now those signals which the controller can send...
        elif(head == 'KILL'):
            # this is a user-sent signal to end the thread and kill the client
            pass

        elif(head == 'RECONNECT'):
            # this is a user-sent signal which will cause all clients to sleep
            # and then attempt to reconnect to the same server.
            pass

        # finally, if all else fails,
        else:
            print("[ %30s ] Error: failed to handle signal '%s'" %
                    (self.__client__, head.upper()))


class TournamentServer(Server):
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)


class DeckPopulation():

    def __init__(self):
        super(DeckPopulation, self).__init__()


if __name__ == '__main__':
    parser = SafeConfigParser()
    parser.read('settings.ini')

    connection = Connection(parser.get('mongodb', 'server'))
    global db
    db = None
    exec('db = connection.' + parser.get('mongodb', 'db'))
    global population




