#!/usr/bin/env python2

import socket
import string
import time
import urllib.request as urllib
import hashlib
import pickle
import re

failstrs = ["6c3c293f9b01ec0099aefbd183a366c2",
            "7e2dcb1efb86cd6014ed8cd43a7cc145"]


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
                    s = ' '.join(l[1::]).strip('.')
                    if s not in deck:
                        deck[s] = 0
                    deck[s] += int(l[0])

                except:
                    exit(1)
    return deck

if __name__ == "__main__" or 1:
    address = ("europa.icmb.utexas.edu", 9001)
    conn = socket.socket()
    conn.connect(address)
    delay = 8

    tmplate = "http://essentialmagic.com/Decks/ExportToApprentice.asp?ID=%i"

    while True:
        print("SENDING PROBE...")
        conn.send("NEXT".encode())
        m = str(conn.recv(1024), "utf-8", 'ignore')

        if m == "DONE":
            print("GOT HALT SIGNAL")
            exit(0)

        else:
            i = int(m)
            m = hashlib.md5()
            text = b''
            while 1:
                try:
                    text = urllib.urlopen(urllib.Request((tmplate % i))).read()
                    break
                except Exception:
                    time.sleep(5*60)
                    delay += 4

            m.update(text)
            if m.hexdigest() in failstrs:
                # the web page downloaded was an error code...
                conn.send(("FAIL %i" % i).encode())

            else:
                # the web page downloaded was OKAY
                text = str(text, 'utf-8', 'ignore')
                print(text)
                print(m.hexdigest())
                d = parse(text)
                b = pickle.dumps(d, 2)
                rsp = 0

                for k in range(10):
                    conn.send(("OKAY %i" % len(b)).encode())
                    conn.recv(128)
                    conn.send(b)
                    rsp = int(str(conn.recv(128), 'utf-8', 'ignore'))
                    if(rsp):
                        print("UPLOADED DECK %7i AFTER %2i ATTEMPTS" %(i, k))
                        break

                if(not rsp):
                    print("FAILED TO UPLOAD DECK %7i AFTER 10 ATTEMPTS" %(i))

                time.sleep(delay)
