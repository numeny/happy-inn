#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from tutorial.sql import RhSql

test_RhSql = RhSql()
test_RhSql.select_first_one()
