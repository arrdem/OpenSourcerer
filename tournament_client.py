#!/usr/bin/env python3
# -*- coding: utf-8 *-*
# This file defines a client for evaluating decks on the Magarena engine and
# reporting the results back to a server.
from lib.network.distributed_client import Client
import socket
import json
import os
import re


class TournamentClient(Client):
    def __init__(self, *args, **kwargs):
        Client.__init__(self, *args, **kwargs)
        self.__delay__ = 5
        self.__done_round__ = False
        self.__has_pair__ = False

        self.__a__ = 0
        self.__a_wins__ = 0

        self.__b__ = 0
        self.__b_wins__ = 0

    def run(self):
        while self.__running__:
            try:
                m = str(self.__conn__.recv(1024), "utf-8")
                if m:
                    self.handle(m)

            except socket.timeout:
                self.upkeep()

    def upkeep(self):
        if not self.__has_pair__:
            self.__conn__.send("NEXT".encode())
        else:
            self.__conn__.send(("RESULTS %i %i" % len(self.__data__)).encode())

    def handle(self, m):
        m = m.split(' ', 1)
        if m[0] == 'PAGEID':
            pass
        elif m[0] == 'GOAHEAD':
            pass
        elif m[0] == '1':
            pass
        elif m[0] == '0':
            pass
        elif m[0] == 'RECONNECT':
            pass
        elif m[0] == 'DONE':
            pass

    def run_round(self, d1, d2, path, AI_level=8, AI_type="MMAB", games=5, ):
        """
        This function opens up the subprocess and runs the actual game then
        parses the output returning the results in the format (d1_won, d2_won)
        """
        usage_str = "java -Xmx1G -cp %s magic.DeckStrCal --deck1 %s " +\
                    " --deck2 %s --games --strength %i 2&>/dev/null"
        game = os.popen(usage_str % (path, d1, d2, games, AI_level), os.P_WAIT)

        # game is a file object which will block until the subprocess ends
        # so using it consists only of .read()ing two lines, expected sample
        # lines:
        #    #deck1    ai1    str1    deck2    ai2    str2    games    d1win    d1lose
        #    /home/reid/decks/zachsoulsister.dec    MMAB    6    /home/reid/decks/RB_Pain_60.dec    MMAB    6    10    9    1

        oline = game.readlines()[1]
        oline = oline.split('\t')
        return tuple(map(int, oline[-2:]))


if __name__ == "__main__" or 1:
    client = TournamentClient("europa.icmb.utexas.edu", 9001)
    client.daemon = False
    client.run()

