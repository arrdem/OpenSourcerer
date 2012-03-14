#!/usr/bin/env python2

from lib.network.distributed_client import Client
from urllib.request import Request
import time
import hashlib
import pickle
import re

class EssentialMagicClient(Client):
    __failstrs__ = ["6c3c293f9b01ec0099aefbd183a366c2",
                    "7e2dcb1efb86cd6014ed8cd43a7cc145"]
    __tmplate__ = "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=%i"
    __rsp__ = 'OK'

    def __init__(self, *args, **kwargs):
        Client.__init__(self, *args, **kwargs)

    def upkeep(self):
        self.__conn__.send("NEXT".encode())

    def handle(self, m):
        i = int(m)
        m = hashlib.md5()
        text = urllib.urlopen(Request((tmplate % i))).read()
        m.update(text)

        if m.hexdigest() in self.__failstrs__:
            # the web page downloaded was an error code...
            self.__conn__.send(("FAIL %i" % i).encode())
            return

        else:
            # the web page downloaded was OKAY
            print(text)
            print(m.hexdigest())
            d = parse(text)
            b = pickle.dumps(d).encode()
            rsp = 0

            for k in range(10):
                self.__conn__.send("OKAY %i" % len(b))
                self.__conn__.recv(128)
                self.__conn__.send(b)
                rsp = int(str(self.__conn__.recv(128)).decode("utf-8"))
                if(rsp):
                    print("UPLOADED DECK %7i AFTER %2i ATTEMPTS" %(i, k))
                    break

            if(not rsp):
                print("FAILED TO UPLOAD DECK %7i AFTER 10 ATTEMPTS" %(i))

            time.sleep(3)

    def parse(s):
        deck = {}
        s = re.sub(r'\r\n', '\n', s)
        lines = re.split(r'\n', s)
        for l in lines:
            m = re.match('//', l)
            if m is None:
                l = re.sub(r'SB:  ', '', l)
                l = re.sub(r' +', ' ', l)
                l = re.sub(r'^ +', '', l)
                l = l.split(" ")
                card_name = ' '.join(l[1::])
                count = l[0]

                #print(l,  card_name,  count)
                if l and (not False in [bool(a) for a in l]):
                    try:
                        deck[' '.join(l[1::])] = int(l[0])
                    except:
                        exit(1)
        return deck

if __name__ == "__main__" or 1:
    client = EssentialMagicClient("129.116.45.180", 9001)
    client.start()
