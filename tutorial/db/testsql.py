#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from db.sql import RhSql
from tutorial.rest_home_item import RestHomeItem


test_RhSql = RhSql();
test_RhSql.create_resthome_table_if_neccesary();
item = RestHomeItem()
item["rh_name"] = "北京市房山区"
item["rh_phone"] = "rh_phone_5"
item["rh_location_id"]=100
item["rh_type"] = "rh_type_5"
item["rh_factory_property"] = "rh_factory_property_5"
item["rh_person_in_charge"] = "rh_person_in_charge_5"
#item["rh_establishment_time"] = "2013年1月1日"
item["rh_floor_surface"] = "rh_floor_surface_5"
item["rh_building_area"] = "rh_building_area_5"
item["rh_bednum"] = "100张"
item["rh_for_persons"] = "rh_for_persons_5"
item["rh_charges_extent"] = "rh_charges_extent_5"
item["rh_special_services"] = "rh_special_services_5"
item["rh_contact_person"] = "rh_contact_person_5"
item["rh_address"] = "rh_address_5"
item["rh_url"] = "rh_url_5"
item["rh_transportation"] = "rh_transportation_5"
item["rh_inst_intro"] = "rh_inst_intro_5"
item["rh_facilities"] = "rh_facilities_5"
item["rh_service_content"] = "rh_service_content_5"
item["rh_inst_notes"] = "rh_inst_notes"

RestHomeItem.printSelf(item)
print("--------");
print("rh_location_id" in item)
print(hasattr(item, "mmm"))
print("--------");
RestHomeItem.init_item_field_to_default_if_null(item)
test_RhSql.insert_data(item);
