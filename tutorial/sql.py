#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb

from tutorial.rest_home_item import RestHomeItem

class RhSql(object):
    __sql_create_resthome_table = "CREATE TABLE IF NOT EXISTS rh (\
                rh_id INT UNSIGNED AUTO_INCREMENT,\
                rh_name VARCHAR(500) NOT NULL,\
                rh_phone VARCHAR(200),\
                rh_location_id INT UNSIGNED,\
                rh_type VARCHAR(200),\
                rh_factory_property VARCHAR(200),\
                rh_person_in_charge VARCHAR(200),\
                rh_establishment_time DATE,\
                rh_floor_surface VARCHAR(200),\
                rh_building_area VARCHAR(200),\
                rh_bednum SMALLINT UNSIGNED,\
                rh_for_persons VARCHAR(200),\
                rh_charges_extent VARCHAR(1000),\
                rh_special_services VARCHAR(1000),\
                rh_contact_person VARCHAR(200),\
                rh_address VARCHAR(1000),\
                rh_url VARCHAR(1000),\
                rh_transportation VARCHAR(1000),\
                rh_inst_intro VARCHAR(5000),\
                rh_facilities VARCHAR(1000),\
                rh_service_content VARCHAR(1000),\
                rh_inst_notes VARCHAR(1000),\
                PRIMARY KEY ( rh_id )\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    __sql_select_name = "select * from rh where rh_name=\"{}\";"
    __sql_existed_rh_name = "select 1 from rh where rh_name=\'{}\' limit 1;"

    __sql_insert_data = "insert into rh (\
                    rh_name, rh_phone, rh_location_id,\
                    rh_type, rh_factory_property, rh_person_in_charge,\
                    rh_establishment_time, rh_floor_surface, rh_building_area,\
                    rh_bednum, rh_for_persons, rh_charges_extent,\
                    rh_special_services, rh_contact_person, rh_address,\
                    rh_url, rh_transportation, rh_inst_intro,\
                    rh_facilities, rh_service_content, rh_inst_notes\
                ) VALUES (\
                    \"%s\", \"%s\", %d,\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    %d, \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\");"


    def __init__(self):
        print("")
        print("********* Start sql operation *******")
        self.connect_to_sql()
        self.create_resthome_table_if_neccesary()

    def connect_to_sql(self):
        print("connect_to_sql ...")
        try:
            self.conn = mdb.connect(host='localhost', user='bdg', passwd='3', db ='rh')
            self.cur = self.conn.cursor()
        except mdb.Error, e:
            print "connect_to_sql, Error %d: %s" % (e.args[0], e.args[1])
            self.close_db()
            sys.exit(1)

    def create_resthome_table_if_neccesary(self):
        print("create_resthome_table_if_neccesary ...")
        self.excute_sql(RhSql.__sql_create_resthome_table)

    def select_name(self, resthome_name):
        print("select_name ...")
        sql_str = RhSql.__sql_select_name
        self.excute_sql(sql_str.format(resthome_name))
        return self.cur.fetchone()

    def existed_rh_name(self, resthome_name):
        print("existed_rh_name ...")
        sql_str = RhSql.__sql_existed_rh_name
        print("existed_rh_name-1 ...%s" % sql_str)
        sql_str = sql_str.format(resthome_name)
        print("existed_rh_name-1-2 ...%s" % sql_str)
        self.excute_sql(sql_str.format(resthome_name))
        print("existed_rh_name-2 ...")
        return self.cur.fetchone()

    def insert_data(self, item):
        print("insert_data ...")
        RestHomeItem.init_item_field_to_default_if_null(item)

        #if self.existed_rh_name(item["rh_name"]) is not None:
        if self.existed_rh_name("bdg") is not None:
            print("[Warnning] the following resthome is existed:")
            RestHomeItem.printSelf(item)
            return

        sql_str = RhSql.__sql_insert_data
        print("sql_str-------------------------------1")
        print(sql_str)
        print("sql_str-------------------------------1-1")
        RestHomeItem.printSelf(item)
        print("sql_str-------------------------------1-2")
        sql_str = (sql_str % (\
                    item["rh_name"], item["rh_phone"], item["rh_location_id"],\
                    item["rh_type"], item["rh_factory_property"], item["rh_person_in_charge"],\
                    item["rh_establishment_time"], item["rh_floor_surface"], item["rh_building_area"],\
                    item["rh_bednum"], item["rh_for_persons"], item["rh_charges_extent"],\
                    item["rh_special_services"], item["rh_contact_person"], item["rh_address"],\
                    item["rh_url"], item["rh_transportation"], item["rh_inst_intro"],\
                    item["rh_facilities"], item["rh_service_content"], item["rh_inst_notes"]))
        self.excute_sql(sql_str)


    def excute_sql(self, sql_str):
        print("------sql_str------")
        print(sql_str)
        try:
            self.cur.execute(sql_str)
            self.conn.commit()
            print("------sql_str------insert ok")
        except Exception as e:
            print("------sql_str------execute Exception:")
            print(e)
            self.conn.rollback()
            self.close_db()
            sys.exit(1)

    def close_db(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
