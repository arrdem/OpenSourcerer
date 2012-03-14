#!/usr/bin/env python3
# This file extends the client in lib.network.client

from lib.network.distributed_client import Client
from lib.card.card import Card
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
import time
import hashlib
import pickle
import re

class GathererClient(Client):
    __failstrs__ = ["2cb5f52b7de8f981bbe74c8b81faf7a4"]
    __tmplate__ = "http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%i"
    __rsp__ = 'OK'

    def __init__(self, *args, **kwargs):
        Client.__init__(self, *args, **kwargs)

    def upkeep(self):
        self.__conn__.send("NEXT".encode())

    def handle(self, m):
        i = int(m)
        m = hashlib.md5()
        text = ""
        try:
            text = str(urlopen(Request((self.__tmplate__ % i))).read(), "utf-8")

        except HTTPError:
            self.__conn__.send(("FAIL %i" % i).encode())
            print("FAILED CARD ID %i" % i)
            return

        except Exception as e:
            print(e)
            exit(1)

        # the web page downloaded was OKAY
        print("GOT CARD %i, HASH %s" % (i, m.hexdigest()))
        text = re.sub(r'', '-', text)
        c = Card(None)
        try:
            c.loadFromGatherer(text)
        except Exception:
            self.__conn__.send(("FAIL %i" % i).encode())
            print("FAILED WHILE PARSING CARD ID %i" % i)
            return

        b = pickle.dumps(c.export())
        rsp = 0

        for k in range(10):
            self.__conn__.send(("OKAY %i" % len(b)).encode())
            self.__conn__.recv(128)
            self.__conn__.send(b)
            rsp = int(str(self.__conn__.recv(128), "utf-8"))
            if(rsp):
                print("UPLOADED CARD %7i AFTER %2i ATTEMPTS" % (i, k))
                break

        if(not rsp):
            print("FAILED TO UPLOAD CARD %7i AFTER 10 ATTEMPTS" % (i))

        time.sleep(3)

if __name__ == "__main__" or 1:
    client = GathererClient("laptop.mckenzielabs.org", 9001)
    client.start()
    input()
    client.join()

