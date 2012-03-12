#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import re

class HTMLTree():
    __id_counter__ = 1
    def __init__(self, *args, **kwargs):
        self.__children__   = []
        self.__fields__     = {'data':'', '_tree_id':int(self.__id_counter__)}
        self.__parent__     = None
        self.__id_counter__ += 1

    def __getitem__(self, key):
        if key in self.__fields__:
            return self.__fields__[key]
        else:
            return None

    def __setitem__(self, key, value):
        self.__fields__[key] = value

    def __str__(self, long = 0):
        if(long == 0):
            return self.__fields__['_type']
        elif(long == 1):
            return str(self.__fields__)
        elif(long > 1):
            self.__fields__['_type'] + "\n".join([str(a) for a in self.__children__])

    def find(self, f):
        """
        All I'm going to say about this method is that while it does a
        revolting O(n) search of the graph (has to, no order) it can
        take any number of really cute lambda functions for f ;-)
        """
        l = self.__children__ + ([self] if self.__parent__ == None else [])
        for node in l:
            if(f(node.__fields__)):
                yield node

        for c in self.__children__:
            for n in c.find(f):
                yield n

    def join(self, recursive=False, field=lambda x: (x if 'data' not in x else x['data'])):
        return field(self) + (' '.join([c.join(recursive=True, field=field)
                                                    for c in self.__children__])
                                            if recursive else '')

class WebPage(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        # set up locals..
        self.__tree_root__ = HTMLTree()
        self.__cursor__ = self.__tree_root__

    def handle_starttag(self, tag, attrs):
        t = HTMLTree()
        self.__cursor__.__children__.append(t)
        t.__parent__ = self.__cursor__
        self.__cursor__ = t
        self.__cursor__['_type'] = tag
        d = dict(attrs)
        self.__cursor__.__fields__.update(d)
        if 'alt' in d:
            self.__cursor__.__parent__['data'] += " %s " % d['alt']

    def handle_endtag(self, tag):
        if self.__cursor__.__parent__:
            self.__cursor__ = self.__cursor__.__parent__

    def handle_data(self, data):
        self.__cursor__['data'] += data

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        pass

if __name__ == "__main__":
    parser = WebPage()
    parser.feed("")

    tree = parser.__tree_root__
    g = tree.search(lambda x: 'id' in x and x['id']=="ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_rarityRow")
    r1 = next(g)
    c1 = re.sub(r'[ \t\r\n]+', ' ', r1.join(recursive=True))
    c1 = re.sub(r'^ *','',c1)
    print(repr(c1))
