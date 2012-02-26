#!/usr/bin/env python


class c(object):

    def __init__(self):
        pass

    def eval(self, s):
        return eval(s)

a = c()
a.eval("self.f = lambda x: return int(x)+1")
print a.f(1)


