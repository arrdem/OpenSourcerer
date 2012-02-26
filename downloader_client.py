#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  downloader_client.py

import socket

HOST = 'europa.icmb.utexas.edu'    # The remote host
PORT = 50007                       # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def sendr(s):
    try:
        s.connect((HOST, PORT))
        s.sendall(s)
        return s.recv(1024)
    finally:
        s.close()

if __name__ == "__main__" or 1:
    while True:
        orders = sendr("NEXT")
        # PARSE the ORDERS string...
        if orders == "DONE":
            # this is the halt case
            sendr("DONE")
            break
        elif orders:
            # DOWNLOAD HERE
            i = long(orders)

        else:
            # something is wrong and we got no data from the server...
            print "No signal from server, exiting..."
            exit(1)
