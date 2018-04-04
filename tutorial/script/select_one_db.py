#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql
from tutorial.rest_home_item import RestHomeItem

test_RhSql = RhSql()
result = test_RhSql.select_first_one()
if result is None:
    print("")
    print("No record existed!")
    exit(1)
RestHomeItem.printOneRecord(result)
