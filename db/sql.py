#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb

sys.path.append("./")
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import my_log
logger = my_log.get_my_logger()

class RhSql(object):
    __sql_create_resthome_table = "CREATE TABLE IF NOT EXISTS rh (\
                rh_id INT UNSIGNED AUTO_INCREMENT,\
                rh_name VARCHAR(500) NOT NULL,\
                rh_phone TEXT,\
                rh_mobile TEXT,\
                rh_email TEXT,\
                rh_postcode TEXT,\
                rh_location_id TEXT,\
                rh_type TEXT,\
                rh_factory_property TEXT,\
                rh_person_in_charge TEXT,\
                rh_establishment_time TEXT,\
                rh_floor_surface TEXT,\
                rh_building_area TEXT,\
                rh_bednum TEXT,\
                rh_staff_num TEXT,\
                rh_for_persons TEXT,\
                rh_charges_extent TEXT,\
                rh_special_services TEXT,\
                rh_contact_person TEXT,\
                rh_address TEXT,\
                rh_url TEXT,\
                rh_transportation TEXT,\
                rh_inst_intro TEXT,\
                rh_inst_charge TEXT,\
                rh_facilities TEXT,\
                rh_service_content TEXT,\
                rh_inst_notes TEXT,\
                rh_ylw_id TEXT,\
                PRIMARY KEY ( rh_id )\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    __sql_select_name = "select * from rh where rh_name=\"{}\";"
    __sql_select_all = "select * from rh;"
    __sql_select_count = "select count(*) from rh;"
    __sql_select_all_rh_ylw_id = "select rh_ylw_id from rh;"
    __sql_select_one_rh_ylw_id = "select * from rh where rh_ylw_id=\"{}\";"

    __sql_delete_all = "delete from rh;"
    __sql_drop_table = "drop table rh;"
    __sql_existed_rh_name = "select 1 from rh where rh_name=\'{}\' and rh_ylw_id=\'{}\' limit 1;"

    __sql_insert_data = "insert into rh (\
                    rh_name, rh_phone, rh_location_id,\
                    rh_mobile, rh_email, rh_postcode,\
                    rh_type, rh_factory_property, rh_person_in_charge,\
                    rh_establishment_time, rh_floor_surface, rh_building_area,\
                    rh_bednum, rh_for_persons, rh_charges_extent,\
                    rh_special_services, rh_contact_person, rh_address,\
                    rh_url, rh_transportation, rh_inst_intro,\
                    rh_inst_charge, rh_facilities, rh_service_content,\
                    rh_inst_notes, rh_ylw_id, rh_staff_num\
                ) VALUES (\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
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
        self.excute_sql(RhSql.__sql_create_resthome_table)

    def select_name(self, resthome_name):
        logger.debug("select_name ...")
        sql_str = RhSql.__sql_select_name
        self.excute_sql(sql_str.format(resthome_name))
        return self.cur.fetchone()

    def select_all(self):
        logger.debug("select_all ...")
        sql_str = RhSql.__sql_select_all
        self.excute_sql(sql_str)
        results = self.cur.fetchall()
        return results

    def select_all_rh_ylw_id(self):
        logger.debug("select_all_rh_ylw_id ...")
        sql_str = RhSql.__sql_select_all_rh_ylw_id
        self.excute_sql(sql_str)
        return self.cur.fetchall()

    def select_one_rh_ylw_id(self, rh_ylw_id):
        logger.debug("select_one_rh_ylw_id ...")
        sql_str = RhSql.__sql_select_one_rh_ylw_id
        sql_str = sql_str.format(rh_ylw_id)
        self.excute_sql(sql_str)
        return self.cur.fetchall()

    def select_first_one(self):
        logger.debug("select_all ...")
        sql_str = RhSql.__sql_select_all
        self.excute_sql(sql_str)
        result = self.cur.fetchone()
        return result

    def select_count(self):
        logger.debug("select_count ...")
        sql_str = RhSql.__sql_select_count
        self.excute_sql(sql_str)
        result = self.cur.fetchone()
        print("select_count ... count: %s" % result[0])

    def existed_rh_name(self, resthome_name, rh_ylw_id):
        try:
            sql_str = RhSql.__sql_existed_rh_name
            sql_str = sql_str.format(resthome_name, rh_ylw_id)
            self.excute_sql(sql_str.format(resthome_name))
            return self.cur.fetchone()
        except Exception as e:
            logger.critical("Error: existed_rh_name(), for rh_ylw_id: %s" % rh_ylw_id)
            logger.critical(e)

    def insert_data(self, item):
        try:
            logger.debug("insert_data ...")

            ret = self.existed_rh_name(item["rh_name"], item["rh_ylw_id"])
            if ret is not None:
                logger.warning("the following resthome is existed: %s, %s" % (item["rh_name"].decode(), item["rh_ylw_id"].decode()))
                return

            sql_str = RhSql.__sql_insert_data
            sql_str = (sql_str % (\
                        item["rh_name"], item["rh_phone"], item["rh_location_id"],\
                        item["rh_mobile"], item["rh_email"], item["rh_postcode"],\
                        item["rh_type"], item["rh_factory_property"], item["rh_person_in_charge"],\
                        item["rh_establishment_time"], item["rh_floor_surface"], item["rh_building_area"],\
                        item["rh_bednum"], item["rh_for_persons"], item["rh_charges_extent"],\
                        item["rh_special_services"], item["rh_contact_person"], item["rh_address"],\
                        item["rh_url"], item["rh_transportation"], item["rh_inst_intro"],\
                        item["rh_inst_charge"], item["rh_facilities"], item["rh_service_content"],\
                        item["rh_inst_notes"], item["rh_ylw_id"], item["rh_staff_num"]))

            self.excute_sql(sql_str)
        except Exception as e:
            logger.critical("Error: insert_data(), for rh_ylw_id: %s" % item['rh_ylw_id'])
            logger.critical(e)

    def delete_all(self):
        logger.debug("delete_all ...")
        sql_str = RhSql.__sql_delete_all
        self.excute_sql(sql_str)

    def drop_table(self):
        logger.debug("drop_table ...")
        sql_str = RhSql.__sql_drop_table
        self.excute_sql(sql_str)

    def excute_sql(self, sql_str):
        logger.debug("starting excute sql_str: %s" % sql_str.decode())
        try:
            self.cur.execute(sql_str)
            self.conn.commit()
            logger.info("excute sql_str : ok")
            print("excute sql_str : ok")
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
