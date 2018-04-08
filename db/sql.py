#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb as mdb

sys.path.append("./")

class RhSql(object):
    __sql_create_resthome_table = "CREATE TABLE IF NOT EXISTS rh (\
                rh_id INT UNSIGNED AUTO_INCREMENT,\
                rh_name VARCHAR(500) NOT NULL,\
                rh_phone VARCHAR(200),\
                rh_mobile VARCHAR(200),\
                rh_email VARCHAR(200),\
                rh_postcode VARCHAR(200),\
                rh_location_id VARCHAR(200),\
                rh_type VARCHAR(200),\
                rh_factory_property VARCHAR(200),\
                rh_person_in_charge VARCHAR(200),\
                rh_establishment_time DATE,\
                rh_floor_surface VARCHAR(200),\
                rh_building_area VARCHAR(200),\
                rh_bednum SMALLINT UNSIGNED,\
                rh_staff_num SMALLINT UNSIGNED,\
                rh_for_persons VARCHAR(200),\
                rh_charges_extent VARCHAR(1000),\
                rh_special_services VARCHAR(1000),\
                rh_contact_person VARCHAR(200),\
                rh_address VARCHAR(1000),\
                rh_url VARCHAR(1000),\
                rh_transportation TEXT,\
                rh_inst_intro TEXT,\
                rh_inst_charge TEXT,\
                rh_facilities TEXT,\
                rh_service_content TEXT,\
                rh_inst_notes TEXT,\
                rh_ylw_id VARCHAR(50),\
                PRIMARY KEY ( rh_id )\
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"

    __sql_select_name = "select * from rh where rh_name=\"{}\";"
    __sql_select_all = "select * from rh;"
    __sql_select_count = "select count(*) from rh;"
    __sql_select_all_rh_ylw_id = "select rh_ylw_id from rh;"
    __sql_select_one_rh_ylw_id = "select * from rh where rh_ylw_id=\"{}\";"

    __sql_delete_all = "delete from rh;"
    __sql_drop_table = "drop table rh;"
    __sql_existed_rh_name = "select 1 from rh where rh_name=\'{}\' limit 1;"

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
                    %d, \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", \"%s\",\
                    \"%s\", \"%s\", %d\
                    );"


    def __init__(self):
        print("")
        print("********* Start sql operation *******")
        self.connect_to_sql()
        self.create_resthome_table_if_neccesary()
        self.excute_sql("set names utf8;")

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

    def select_all(self):
        print("select_all ...")
        sql_str = RhSql.__sql_select_all
        self.excute_sql(sql_str)
        results = self.cur.fetchall()
        return results

    def select_all_rh_ylw_id(self):
        print("select_all_rh_ylw_id ...")
        sql_str = RhSql.__sql_select_all_rh_ylw_id
        self.excute_sql(sql_str)
        return self.cur.fetchall()

    def select_one_rh_ylw_id(self, rh_ylw_id):
        print("select_one_rh_ylw_id ...")
        sql_str = RhSql.__sql_select_one_rh_ylw_id
        sql_str = sql_str.format(rh_ylw_id)
        self.excute_sql(sql_str)
        return self.cur.fetchall()

    def select_first_one(self):
        print("select_all ...")
        sql_str = RhSql.__sql_select_all
        self.excute_sql(sql_str)
        result = self.cur.fetchone()
        return result

    def select_count(self):
        print("select_count ...")
        sql_str = RhSql.__sql_select_count
        self.excute_sql(sql_str)
        result = self.cur.fetchone()
        print("select_count ... count: %s" % result[0])

    def existed_rh_name(self, resthome_name):
        sql_str = RhSql.__sql_existed_rh_name
        sql_str = sql_str.format(resthome_name)
        self.excute_sql(sql_str.format(resthome_name))
        return self.cur.fetchone()

    def insert_data(self, item):
        print("insert_data ...")

        ret = self.existed_rh_name(item["rh_name"])
        if ret is not None:
            print("[Warnning] the following resthome is existed: %s, %s" % item["rh_name"], item["rh_ylw_id"])
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

    def delete_all(self):
        print("delete_all ...")
        sql_str = RhSql.__sql_delete_all
        self.excute_sql(sql_str)

    def drop_table(self):
        print("drop_table ...")
        sql_str = RhSql.__sql_drop_table
        self.excute_sql(sql_str)

    def excute_sql(self, sql_str):
        print("starting excute sql_str")
        print(sql_str)
        try:
            self.cur.execute(sql_str)
            self.conn.commit()
            print("excute sql_str : ok")
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
