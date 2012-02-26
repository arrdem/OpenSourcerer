#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  downloader_server.py

import socket
import curses
import time
import subprocess

global hosts, start_time, counter

HOST        = ''                # Symbolic name meaning all available interfaces
PORT        = 50007             # Arbitrary non-privileged port
hosts       = []
start_time  = None
counter     = 0


def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()


def ui():
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)


if __name__ == "__main__" or 1:
    # record start time...
    start_time = time.time()

    # launch the two threads...



