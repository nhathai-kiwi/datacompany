#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import os
import urllib
import mysql.connector
from mysql.connector import errorcode
import time

# dinh dang file output
out_name_txt = 'congty%s.txt'
out_name_json = 'congty%s.json'


# duong dan cua cac folder
path = os.path.dirname(os.path.abspath(__file__))
save_path_txt = path.replace('/src', '/txt')
save_path_json = path.replace('/src', '/json')


config = {
    'user': 'root',
    'password': 'root',
    'port': '8889',
    'host': '127.0.0.1',
    'database': 'information_company',
}


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


# TABLES: dict
TABLES = {}
TABLES['companies'] = (
    "CREATE TABLE `companies` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` TEXT,"
    "  `address` TEXT," 
    "  `legal_representative` TEXT,"
    "  `issue_date` TEXT,"
    "  `date_of_operation` TEXT,"
    "  `tax_code` TEXT,"
    "  `phone` TEXT,"
    "  `url` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


# tao ra tat ca table co trong dict: TABLES
def create_table():
    for name, ddl in TABLES.iteritems():
        print name
        print ddl
        try:
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            pass
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                 print("already exists.")
            else:
                 print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()
    return 0
# DONE


# them ki tu dac biet vao trc dau '
def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    return s


# doc file json chua du lieu cac cong ty roi insert vao table companies
def insert_company_from_json(out_json_files):

    for item in out_json_files:
        out_json = item[0]
        start_id = item[1]
        print "File insert: ", out_json
        with open(out_json) as json_data:
            d = json.load(json_data)
            items = d['item']
            for item in items:
                name = addslashes(item['name'])
                address = addslashes(item['address'])
                legal_representative = addslashes(item['legal_representative'])
                issue_date = addslashes(item['issue_date'])
                date_of_operation = addslashes(item['date_of_operation'])
                tax_code = addslashes(item['tax_code'])
                phone = addslashes(item['phone'])
                url = addslashes(item['url'])
                # print address, name, url
                query = "INSERT INTO companies(id, name, address, legal_representative, issue_date, date_of_operation, tax_code, phone, url) " \
                        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (start_id, name, address, legal_representative, issue_date, date_of_operation, tax_code, phone, url)
                # print query
                cursor.execute(query)
                cnx.commit()
                start_id += 1

        print "Part 03 Done: ", out_json


    cursor.close()
    cnx.close()

    return 0

