#!/usr/bin/env python3
# -*- coding: utf-8 *-*
from lib.network.distributed_server import Server, connectionThread

from pymongo.connection import Connection
from configparser import SafeConfigParser
import threading
import socket
import pickle
import os
import re


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

        self.__grammar__ = re.Scanner([
            (r'(?<=DONE )(1|0)', lambda x, y: ('DONE', y, self.__logwin__)),
            (r'NEXT', lambda x, y: ('NEXT', y, self.__next__)),
            (r'(?<=ERROR )((RECV)|(RUN))', lambda x, y: ('ERROR', y,
                                                         self.__err__)),
            ])

        # the IDs of the decks being evaluated on the client
        self.__a__ = None
        self.__b__ = None

        self.__queue__ = []

    def __logwin__(self, id):
        """
        Used to record which deck won the series
        """
        global population
        if(id == 0):
            population.logGame(self.__a__, self.__b__)
        elif(id == 1):
            population.logGame(self.__b__, self.__a__)
        else:
            raise Exception("Unexpexted value in __logwin__: %i" % (id))

    def __next__(self):
        """
        Used to generate and send the next pair of decks to the client.
        """



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
    db = None
    exec('db = connection.' + parser.get('mongodb', 'db'))

    global population




