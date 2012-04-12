#!/usr/bin/env python

from pymongo.connection import Connection

connection = Connection("146.6.213.39")
db = connection.magic
# DB users.. 'fizzard', 'dwagon' - no admin
# DB users.. 'maint', 'M#1IMUkmfp2D' - admin
db.auth('maint', 'M#1IMUkmfp2D')

cursor = db.cards.find()
for d in cursor:
    print d
