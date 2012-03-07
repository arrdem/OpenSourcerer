#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is a post-processing script I contrived to study the distribution
# of community ratings. The idea is to get a handle on whether the
# community tends to upvote good cards or whether there is a nash
# equilibrium where angry players begin to interfere with the 5.0 rating 

from __future__ import division
import matplotlib
import mcardlib
import re

def avg(x):
    return sum(x)/len(x)

lib = mcardlib.load()

raw_ratings = [i[u'Community Rating:'] for i in lib]
votes = [i[u'Community Votes:'] for i in lib]
adj_rating = [i[u'Meta Rating:'] for i in lib]

print "raw rating:", avg(raw_ratings),"  ",min(raw_ratings),"  ",max(raw_ratings)
print "votes     :", avg(votes),"  ",min(votes),"  ",max(votes)
print "new rating:", avg(adj_rating),"  ",min(adj_rating),"  ",max(adj_rating)

