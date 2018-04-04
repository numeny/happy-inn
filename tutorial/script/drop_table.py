#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql

test_RhSql = RhSql()
test_RhSql.drop_table()
