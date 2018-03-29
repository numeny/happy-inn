#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb

from tutorial.rest_home_item import RestHomeItem

class RhSql(object):
    __sql_create_resthome_table = "CREATE TABLE IF NOT EXISTS resthome (\
                rh_id INT UNSIGNED AUTO_INCREMENT,\
                rh_name VARCHAR(100) NOT NULL,\
                rh_phone VARCHAR(40),\
                rh_location_id INT UNSIGNED,\
                rh_type VARCHAR(40),\
                rh_factory_property VARCHAR(40),\
                rh_person_in_charge VARCHAR(40),\
                rh_establishment_time DATE,\
                rh_floor_surface VARCHAR(40),\
                rh_building_area VARCHAR(40),\
                rh_bednum SMALLINT UNSIGNED,\
                rh_for_persons VARCHAR(40),\
                rh_charges_extent VARCHAR(40),\
                rh_special_services VARCHAR(100),\
                rh_contact_person VARCHAR(40),\
                rh_address VARCHAR(200),\
                rh_url VARCHAR(100),\
                rh_transportation VARCHAR(200),\
                rh_inst_intro VARCHAR(10000),\
                rh_facilities VARCHAR(1000),\
                rh_service_content VARCHAR(1000),\
                rh_inst_notes VARCHAR(1000),\
                PRIMARY KEY ( rh_id )\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    __sql_select_name = "select * from resthome where rh_name=\"{}\";"
    __sql_existed_rh_name = "select 1 from resthome where rh_name=\'{}\' limit 1;"

    __sql_insert_data = "insert into resthome (\
                    rh_name, rh_phone, rh_location_id,\
                    rh_type, rh_factory_property, rh_person_in_charge,\
                    rh_establishment_time, rh_floor_surface, rh_building_area,\
                    rh_bednum, rh_for_persons, rh_charges_extent,\
                    rh_special_services, rh_contact_person, rh_address,\
                    rh_url, rh_transportation, rh_inst_intro,\
                    rh_facilities, rh_service_content, rh_inst_notes\
                ) VALUES (\
                    \"{}\", \"{}\", {},\
                    \"{}\", \"{}\", \"{}\",\
                    \"{}\", \"{}\", \"{}\",\
                    {}, \"{}\", \"{}\",\
                    \"{}\", \"{}\", \"{}\",\
                    \"{}\", \"{}\", \"{}\",\
                    \"{}\", \"{}\", \"{}\");"


    def __init__(self):
        self.connect_to_sql()
        self.create_resthome_table_if_neccesary()

    def connect_to_sql(self):
        print("connect_to_sql ...")
        try:
            self.conn = mdb.connect(host='localhost', user='bdg', passwd='3', db ='resthome')
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
        self.init_item_if_neccesary(item)

        #if self.existed_rh_name(item["rh_name"]) is not None:
        if self.existed_rh_name("bdg") is not None:
            print("[Warnning] the following is existed!")
            RestHomeItem.printSelf(item)
            return

        sql_str = RhSql.__sql_insert_data
        print("sql_str-------------------------------1")
        print(sql_str)
        sql_str = sql_str.format(\
                    item["rh_name"], item["rh_phone"], item["rh_location_id"],\
                    item["rh_type"], item["rh_factory_property"], item["rh_person_in_charge"],\
                    item["rh_establishment_time"], item["rh_floor_surface"], item["rh_building_area"],\
                    item["rh_bednum"], item["rh_for_persons"], item["rh_charges_extent"],\
                    item["rh_special_services"], item["rh_contact_person"], item["rh_address"],\
                    item["rh_url"], item["rh_transportation"], item["rh_inst_intro"],\
                    item["rh_facilities"], item["rh_service_content"], item["rh_inst_notes"])
        print("sql_str-------------------------------2")
        print(sql_str)
        self.excute_sql(sql_str)

    def init_item_if_neccesary(self, item):
        for i in RestHomeItem.item_list:
            if i not in item:
                item[i] = RestHomeItem.item_list[i]

    def excute_sql(self, sql_str):
        print("------sql_str------")
        print(sql_str)
        try:
            self.cur.execute(sql_str)
            self.conn.commit()
        except mdb.Error, e:
            print("------sql_str------")
            print "Error %d: %s" % (e.args[0], e.args[1])
            print(sql_str)
            self.conn.rollback()
            self.close_db()
            sys.exit(1)

    def close_db(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
