#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../../")

import MySQLdb as mdb
from tutorial.sql import RhSql
from tutorial.rest_home_item import RestHomeItem


test_RhSql = RhSql();
test_RhSql.create_resthome_table_if_neccesary();
rhi = RestHomeItem()
rhi["rh_name"] = "北京市房山区普乐园爱心养老院"
rhi["rh_phone"] = "rh_phone_5"
rhi["rh_location_id"]=100
rhi["rh_type"] = "rh_type_5"
rhi["rh_factory_property"] = "rh_factory_property_5"
rhi["rh_person_in_charge"] = "rh_person_in_charge_5"
rhi["rh_floor_surface"] = "rh_floor_surface_5"
rhi["rh_building_area"] = "rh_building_area_5"
rhi["rh_for_persons"] = "rh_for_persons_5"
rhi["rh_charges_extent"] = "rh_charges_extent_5"
rhi["rh_special_services"] = "rh_special_services_5"
rhi["rh_contact_person"] = "rh_contact_person_5"
rhi["rh_address"] = "rh_address_5"
rhi["rh_url"] = "rh_url_5"
rhi["rh_transportation"] = "rh_transportation_5"
rhi["rh_inst_intro"] = "rh_inst_intro_5"
rhi["rh_facilities"] = "rh_facilities_5"
rhi["rh_service_content"] = "rh_service_content_5"

print("--------");
print("rh_location_id" in rhi)
print(hasattr(rhi, "mmm"))
print("--------");
test_RhSql.insert_data(rhi);
