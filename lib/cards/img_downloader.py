#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

muids = [int(i) for i in open("./muids.dat")]

os.chdir("./img/")

for i in muids:
    os.system("wget -O ./"+str(i)+".jpeg http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+str(i)+"\&type=card")
