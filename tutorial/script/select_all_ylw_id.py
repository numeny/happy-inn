#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql


test_RhSql = RhSql()
ret = test_RhSql.select_all_rh_ylw_id()
print(ret)
