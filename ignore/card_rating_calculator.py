#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is a post-processing script I contrived to add some more data to
# the standard cards.dat file by expanding the "Community Rating:"
# value into "Community Rating:", "Community Votes:" and "Meta Rating:"
#
# Meta Rating is the community rating multiplied by the votes.
# the idea is that it reflects both the popularity (or hatred) of the
# card and thereby is some measure of its efficacy in play.

from __future__ import division
import matplotlib
import mcardlib
import re

def avg(x):
    return sum(x)/len(x)

lib = mcardlib.load()

for i in xrange(len(lib)):
    j = lib[i][u'Community Rating:']
    j = re.sub(re.compile("[()A-Za-z:\s]"), '',j)
    f = j.split("/")
    lib[i][u'Community Rating:'], lib[i][u'Community Votes:'], lib[i][u'Meta Rating:'] = float(f[0]), int(f[1]), int(f[1])*float(f[0])

print len(lib)
print lib[15]

of = open("./cards_2.dat", 'w')
for foo in lib:
    of.write(repr(foo)+"\n")

"""raw_ratings = [ratings[i][0] for i in ratings]
votes = [ratings[i][1] for i in ratings]
adj_rating = [ratings[i][2] for i in ratings]

print "raw rating:", avg(raw_ratings),"  ",min(raw_ratings),"  ",max(raw_ratings)
print "votes     :", avg(votes),"  ",min(votes),"  ",max(votes)
print "new rating:", avg(adj_rating),"  ",min(adj_rating),"  ",max(adj_rating)"""

