#!/usr/bin/env python3
import threading
import socket
import string

class Client(threading.Thread):
    """
    A slave node to a subclass/implimentation of the server found in
    distributed_server.py
    """

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.__running__ = True

        self.__host__ = host
        self.__port__ = port
        self.__conn__ = socket.socket()
        self.__conn__.connect((host, port))
        self.__conn__.settimeout(2.0)

    def join(self):
        self.__running__ = False
        try:
            threading.Thread.join(self)
        except:
            return

    def run(self):
        while self.__running__:
            try:
                m = str(self.__conn__.recv(1024), "utf-8")
                if m:
                    self.handle(m)
            except socket.timeout:
                self.upkeep()

    def upkeep(self):
        self.__conn__.send("ONLINE".encode())

    def handle(self, message):
        print("Recieved message: \"%s\"" % message)

