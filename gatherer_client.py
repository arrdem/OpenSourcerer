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

    def upkeep(self):
        self.__conn__.send("NEXT".encode())

    def handle(self, m):
        i = int(m)
        text = ""
        try:
            text = str(urlopen(Request((self.__tmplate__ % i))).read(), "utf-8")

        except HTTPError:
            self.__conn__.send(("FAIL %i" % i).encode())
            print("FAILED CARD ID %i, REDIRECT" % i)
            return

        except Exception as e:
            print(e)
            exit(1)

        # the web page downloaded was OKAY
        print("GOT CARD %i" % (i))
        text = re.sub(r'', '-', text)
        c = Card(None)
        tree = None
        try:
            tree = c.loadFromGatherer(text)
        except:
            cursor = tree
            while 1:
                m = input("DEBUG > ").split()
                if m[0] == 'l':
                    print(' '.join(a.__str__() for a in cursor.__children__))
                elif m[0] == 'g':
                    cursor = cursor.__children__[int(m[1])]
                elif m[0] == 'u':
                    cursor = cursor.__parent__
                else:
                    try:
                        exec(' '.join(m))
                    except:
                        continue

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

        time.sleep(self.__delay__)

if __name__ == "__main__" or 1:
    client = GathererClient("laptop.mckenzielabs.org", 9001)
    client.start()
    input()
    client.join()

