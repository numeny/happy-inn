#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql
from tutorial.rest_home_item import RestHomeItem

test_RhSql = RhSql()
results = test_RhSql.select_all()
for r in results:
    RestHomeItem.printOneRecord(r)
