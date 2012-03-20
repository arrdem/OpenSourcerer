#!/usr/bin/env python3
# This file extends the client in lib.network.client

from lib.network.distributed_client import Client
from lib.card.card import Card
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
import time
import pickle
import re

class GathererClient(Client):
    __failstrs__ = ["2cb5f52b7de8f981bbe74c8b81faf7a4"]
    __tmplate__ = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%i"
    __rsp__ = 'OK'

    def __init__(self, *args, **kwargs):
        Client.__init__(self, *args, **kwargs)
        self.__delay__ = 5
        self.__has_deck__ = False
        self.__data__ = b''

    def upkeep(self):
        if not self.__has_deck__:
            self.__conn__.send("NEXT".encode())
        else:
            self.__conn__.send(("OKAY %i" % len(self.__data__)).encode())

    def handle(self, m):
        m = m.split(' ',1)

        if m[0] == 'PAGEID'
            i = int(m[1])
            text = ""
            try:
                text = str(urlopen(Request((self.__tmplate__ % i))).read(), "utf-8")
                print("GOT CARD %i" % (i))
                text = re.sub(r'', '-', text)
                c = Card(None)
                tree = None
                tree = c.loadFromGatherer(text)
                self.__data__ = pickle.dumps(c.export())

            except HTTPError:
                self.__conn__.send(("FAIL %i" % i).encode())
                print("FAILED CARD ID %i, REDIRECT" % i)
                return

            except RuntimeError as e:
                msg = "FAILED TO PARSE DECK, '%s'" % str(e)
                self.__conn__.send(("FAIL %i %s" % (i, msg).encode())
                print(msg)
                return

            except Exception as e:
                print(e)
                self.__conn__.send(("FATAL %s" % str(e)).encode())
                self.__conn__.close()
                self.join()

        elif m[0] == 'GOAHEAD':
            self.__conn__.send(self.__data__)
            self.__conn__.recv(128)
            self.__conn__.send(b)
            rsp = int(str(self.__conn__.recv(128), "utf-8"))
            if(rsp):
                print("UPLOADED CARD %7i AFTER %2i ATTEMPTS" % (i, k))
                break

        if(not rsp):
            print("FAILED TO UPLOAD CARD %7i AFTER 10 ATTEMPTS" % (i))

        time.sleep(self.__delay__)

if __name__ == "__main__" or 1:
    client = GathererClient("127.0.0.1", 9001)
    client.start()
    input()
    client.join()

