#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       card-downloader.py
#
#       Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#
#       This is a piece of software I threw together after I became
#       interested in MTG which crawls the official card index at
#       http://gatherer.wizards.com/Pages/Card/Details.aspx
#       and downloads the data on cards for writing to a .csv or other
#       analysis. Probably a violation of the official page's EULA, but
#       they don't have a robots.txt I could find, nor a posted EULA.
#       Therefore no holds are bared.

import urllib2
import sys
import re
import hashlib
import os

global __MIDs__
__MIDs__ = set()    # the MIDs of all added cards
__seed_MIDs__= [ # a list of MIDs to start from....
108933,191306,80530,45374,191056,39675,19891,2729,1229,178113,97052,
198386,87913,220955,100,4807,1923,37909,1239,89019,96936,3371,126294,
193511,182270,1665,116747,6550,3315,20225,4851,96873,189272,140183,
226589,247358,206343,194208,213792,243464,242485,244335,244332,244330,
244325,244320]
__consecutive_fails__ = 200
__get_image__ = True
__db_file__ = open('./cards.dat','a')

class EnglishError(Exception):
    pass

try:
    _FailFile = open('./bad.dat')
    _skip += [int(a) for a in _FailFile.readlines()]
except Exception:
    pass
finally:
    _FailFile = open('./bad.dat','a')

__failhash__ = hashlib.md5()
__failhash__.update(''.join(urllib2.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=0").readlines()))
__failhash__ = _failhash.digest()

def isEnglish(string):
    return True in [True for foo in string.split(" ") if foo in [a.strip("\n") for a in open("/usr/share/dict/words")]]

def download(url):
    i = urllib2.urlopen(url).readlines()
    data = u'\n'.join(i)

    h = hashlib.md5()
    h.update(data)
    h = h.digest()

    if(h != __failhash__):
        return data

def parse(l):
    return d

def find_cards(i=0, delta=1):
    global MIDs
    failcount = 0
    z = 0
    while i > 0:
        if not i in MIDs:
            try:
                c = parse(download("http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid="+str(i)))
                c["Multiverse ID:"] = i

                MIDs.append(i)

                #print
                #for foo in c:
                #    print "\t", foo, repr(c[foo])

                try:
                    data = urllib2.urlopen("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+str(c)+"&type=card").read()

                    h = hashlib.md5()
                    h.update(data)

                    c[u"Img MD5Sum:"] = h.hexdigest()

                    c[u"Img File:"] = u"./img/"+unicode(c)+u".jpeg"

                    open(c[u"Img File:"],'wb').write(data)

                except EnglishError:
                    print "\r[!] ENGLISH ERROR IN",i,"                                               "

                except Exception:
                    pass

                failcount = 0

                _DBFile.write(repr(c)+"\n")

            except Exception:
                failcount +=1
                _FailFile.write(str(i)+"\n")
                if failcount >= _ConsecutiveFails:
                    break

            finally:
                i += delta
                if z <= 77:
                    sys.stdout.write("\r["+"="*z+">"+" "*(78-z)+"]  "+str(len(MIDs)))
                    sys.stdout.flush()
                    z+=1
                else:
                    z=0


#if __name__ == "__main__":
#    # this code downloads a set of MUIDs from ./muids.dat
#    import progbar
#    p = progbar.progbar()
#
#    data = [244335,244332,244330,244325,244320]
#
#    for c in data:
#        try:
#            d = parse(download("http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid="+str(c)))
#            d[u"Multiverse ID:"] = c
#
#            data = urllib2.urlopen("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+str(c)+"&type=card").read()
#
#            h = hashlib.md5()
#            h.update(data)
#
#            d[u"Img MD5Sum:"] = h.hexdigest()
#
#            d[u"Img File:"] = u"./img/"+unicode(c)+u".jpeg"
#
#            open(d[u"Img File:"],'wb').write(data)
#
#            MIDs.append(c)
#
#            _DBFile.write(repr(d)+"\n")
#
#        except Exception:
#            print "\r[!] ERROR IN MUID",c," "*60
#
#        finally:
#            p.update()

if __name__ == "__main__":
    # this code just searches for every MUID/card it can find and
    # downloads all of them.
    try:
        for foo in set(_RandKeys+[getMID() for i in range(0,20)]):
            w=len(MIDs)

            find_cards(i = foo, delta = 1)
            find_cards(i = foo-1, delta = -1)

            _DBFile.flush()

            print "\rFINISHED SEARCHING THE SPACE AROUND",foo," FOUND",len(MIDs)-w,"CARDS"+" "*(90-(len(str(foo))+2+len(str(len(MIDs)-w))+2))

    finally:
        mof = open("./muids.dat")
        for id in MIDs:
            mof.write(str(id)+"\n")
        mof.flush()
        _DBFile.flush()
