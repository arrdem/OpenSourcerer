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

from __future__ import division
from BeautifulSoup import BeautifulSoup

import urllib2
import sys
import re
import hashlib
import os

import mcardlib

global MIDs
MIDs=[]    # the MIDs of all added cards

_RandKeys=[ # a list of random MIDs to start from....
108933,191306,80530,45374,191056,39675,19891,2729,1229,178113,97052,
198386,87913,220955,100,4807,1923,37909,1239,89019,96936,3371,126294,
193511,182270,1665,116747,6550,3315,20225,4851,96873,189272,140183,
226589,247358,206343,194208,213792,243464,242485,244335,244332,244330,
244325,244320]

_ConsecutiveFails = 200
_getImage = True
_DBFile = open('./cards.dat','a')

class EnglishError(Exception):
    pass

try:
    _FailFile = open('./bad.dat')
    _skip += [int(a) for a in _FailFile.readlines()]
except Exception: pass
finally:
    _FailFile = open('./bad.dat','a')

_failhash = hashlib.md5()
_failhash.update(''.join(urllib2.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=0").readlines()))
_failhash = _failhash.digest()

def isEnglish(string):
    return True in [True for foo in string.split(" ") if foo in [a.strip("\n") for a in open("/usr/share/dict/words")]]

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def find(data, target):
    """returns the index of the first instance of the object target"""
    try: return [i for i in range(len(data)) if (target in data[i]) or (data[i] == target)][0]
    except Exception: return -1

def getMID(url = "http://gatherer.wizards.com/Pages/Card/Details.aspx?action=random"):
    data = ''.join(urllib2.urlopen(url).readlines())
    data = re.compile("""multiverseid=[0-9]*?\"""").search(data).group(0)
    data = re.sub(re.compile("""\D"""),"",data)
    return int(data)

def download(s):
    i = urllib2.urlopen(s).readlines()
    i = [j.decode("utf-8") for j in i]
    
    #print type(i)
    #for j in range(len(i)):
    #    print j,"\t",i[j],

    data = u''.join(i)
    
    h=hashlib.md5()
    h.update(''.join([d for d in data if ord(d) <= 128]))
    h = h.digest()
    
    if(h != _failhash):
        foo=re.sub(re.compile("""<img src="/Handlers/Image.ashx?.*? alt="|" align.*?/>"""),'',data)
        foo=re.sub(re.compile("""<[^<]+?>"""),"",foo)
        foo=re.sub(re.compile("""<img.*? alt=\""""),"",foo)
        foo=re.sub(re.compile("""&.*?;"""),"",foo)
        foo=re.sub(re.compile("""<|\|"""),"",foo)
        foo=re.sub(re.compile(""" +?""")," ",foo)
        foo=re.sub(re.compile("""\."""),". ",foo)
        foo=re.sub(re.compile("""\r"""),"",foo)
        
        foo.lstrip()
        foo = foo.replace(")",") ")
        foo = [s.lstrip() for s in foo.split("\n") if s.lstrip()][25::]
        
        #for i in range(len(foo)):
        #    print i,"\t",foo[i]
        #print "*"*80+"\n\n"
        
        return foo
    
    else:
        raise Exception

def parse(l):
    d={}
    for key in mcardlib._Keys:
        i=find(l,key)+1
        if (not i == -1) and (not (l[i] in mcardlib._Keys)):
                d[key]=l[i]
        else:
            d[key]=""

    #print 
    #for foo in d:
    #    print "\t", foo, repr(d[foo])

    if not isEnglish(d[u"Card Text:"]):
        raise EnglishError()

    # calculate mana cost
    #[RED, BLUE, BLACK, GREEN, WHITE, ANY, TOTAL]
    try:
        d["Converted Mana Cost:"] = int(d["Converted Mana Cost:"])
    except:
        d["Converted Mana Cost:"] = 0
    d["Mana Cost:"] = [d["Mana Cost:"].count("R"),d["Mana Cost:"].count("U"),d["Mana Cost:"].count("B"),d["Mana Cost:"].count("G"),d["Mana Cost:"].count("W")]
    d["Mana Cost:"].append(d["Converted Mana Cost:"]-sum(d["Mana Cost:"]))
    d["Mana Cost:"].append(d["Converted Mana Cost:"])
    d.pop("Converted Mana Cost:")

    # calculate types
    d["Types:"] = [t for t in d["Types:"].split(" ") if t != '']

    # calculate tags
    d['TAGS'] = [t for t in mcardlib._keywords if t.lower() in d["Card Text:"].lower()]
    bools = [True for foo in d["Mana Cost:"][0:5] if foo]
    if sum(bools) > 1: d['TAGS'].append("Multicolored")

    # calculate P/T
    try:
        d["P/T:"] = [int(g) for g in d["P/T:"].split("/")]
    except Exception:
        d["P/T:"] = [0,0]
    
    # calculate Hand/Life
    try:
        d["Hand/Life:"] = [int(g) for g in d["Hand/Life:"].split("/")]
    except Exception:
        d["Hand/Life:"] = [0,0]

    if d["Loyalty:"] == 'Sets  Legality\r':
        d["Loyalty:"] = ""
        
    if d["Flavor Text:"] == 'Sets  Legality\r':
        d["Flavor Text:"] = ""

    # calculate the ratign information
    j = d[u'Community Rating:']
    j = re.sub(re.compile("[()A-Za-z:\s]"), '',j)
    f = j.split("/")
    d[u'Community Rating:'], d[u'Community Votes:'], d[u'Meta Rating:'] = float(f[0]), int(f[1]), int(f[1])*float(f[0])

    if d[u'Community Votes:'] == 0:
        d[u'Community Rating:'] = 0

    # all done!
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


if __name__ == "__main__":
    # this code downloads a set of MUIDs from ./muids.dat
    import progbar
    p = progbar.progbar()

    data = [244335,244332,244330,244325,244320]
    
    for c in data:            
        try:
            d = parse(download("http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid="+str(c)))
            d[u"Multiverse ID:"] = c

            data = urllib2.urlopen("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid="+str(c)+"&type=card").read()

            h = hashlib.md5()
            h.update(data)
            
            d[u"Img MD5Sum:"] = h.hexdigest()
            
            d[u"Img File:"] = u"./img/"+unicode(c)+u".jpeg"

            open(d[u"Img File:"],'wb').write(data)
            
            MIDs.append(c)

            _DBFile.write(repr(d)+"\n")

        except Exception:
            print "\r[!] ERROR IN MUID",c," "*60

        finally:
            p.update()

if __name__ == "__main__":
    # this code just searches for every MUID/card it can find and 
    # downloads all of them.
    try:
        for foo in set(_RandKeys+[getMID() for i in xrange(0,20)]):
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
