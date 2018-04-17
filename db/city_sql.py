#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb

sys.path.append("./")
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import my_log
logger = my_log.get_my_logger()

class CitySql(object):
    __sql_create_city_table = "CREATE TABLE IF NOT EXISTS city (\
                city_id INT UNSIGNED AUTO_INCREMENT,\
                privince TEXT,\
                city TEXT,\
                area TEXT,\
                PRIMARY KEY ( city_id )\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    __sql_select_name = "select * from city where rh_name=\"{}\";"
    __sql_select_all = "select * from city;"
    __sql_select_count = "select count(*) from city;"

    __sql_delete_all = "delete from city;"
    __sql_drop_table = "drop table city;"
    __sql_existed_city = "select 1 from city where privince=\'{}\' and city=\'{}\' and area=\'{}\' limit 1;"

    __sql_insert_data = "insert into city (\
                    privince, city, area\
                ) VALUES (\
                    \"%s\", \"%s\", \"%s\"\
                    );"


    def __init__(self):
        try:
            logger.info("********* Start sql operation *******")
            self.connect_to_sql()
            self.create_resthome_table_if_neccesary()
            self.excute_sql("set names utf8;")
        except Exception as e:
            logger.critical("Error: sql.py.__init__()")
            logger.critical(e)

    def connect_to_sql(self):
        logger.debug("connect_to_sql ...")
        try:
            self.conn = mdb.connect(host='localhost', user='bdg', passwd='3', db ='rh')
            self.cur = self.conn.cursor()
        except mdb.Error, e:
            logger.critical("connect_to_sql, Error %d: %s" % (e.args[0], e.args[1]))
            self.close_db()
            sys.exit(1)

    def create_resthome_table_if_neccesary(self):
        logger.debug("create_resthome_table_if_neccesary ...")
        self.excute_sql(CitySql.__sql_create_city_table)

    def select_all(self):
        logger.debug("select_all ...")
        sql_str = CitySql.__sql_select_all
        self.excute_sql(sql_str)
        results = self.cur.fetchall()
        return results

    def existed_city(self, p, c, a):
        try:
            sql_str = CitySql.__sql_existed_city
            sql_str = sql_str.format(p, c, a)
            self.excute_sql(sql_str)
            return self.cur.fetchone()
        except Exception as e:
            logger.critical("Error: existed_rh_name(), for rh_ylw_id: %s" % rh_ylw_id)
            logger.critical(e)

    def insert_data(self, item):
        try:
            logger.debug("insert_data ...")

            ret = self.existed_city(item["privince"], item["city"], item["area"])
            if ret is not None:
                logger.warning("the following city is existed: %s, %s" % (item["privince"].decode(), item["city"].decode(), item["area"].decode()))
                return

            sql_str = CitySql.__sql_insert_data
            sql_str = (sql_str % (item["privince"], item["city"], item["area"]))

            self.excute_sql(sql_str)
        except Exception as e:
            logger.critical("Error: insert_data(), for rh_ylw_id: %s" % item['rh_ylw_id'])
            logger.critical(e)

    def delete_all(self):
        logger.debug("delete_all ...")
        sql_str = CitySql.__sql_delete_all
        self.excute_sql(sql_str)

    def drop_table(self):
        logger.debug("drop_table ...")
        sql_str = CitySql.__sql_drop_table
        self.excute_sql(sql_str)

    def excute_sql(self, sql_str):
        logger.debug("starting excute sql_str: %s" % sql_str.decode())
        try:
            self.cur.execute(sql_str)
            self.conn.commit()
            logger.info("excute sql_str : ok")
#print("excute sql_str : ok")
        except Exception as e:
            logger.critical("execute sql Exception: %s" % sql_str)
            logger.critical(e)
            print("execute sql Exception: %s" % sql_str)
            print(e)
            self.conn.rollback()
            self.close_db()
            sys.exit(1)

    def close_db(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

