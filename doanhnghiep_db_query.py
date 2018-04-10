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
    'database': 'enterprises',
}


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()


# TABLES: dict
TABLES = {}

TABLES['companies'] = (
    "CREATE TABLE `companies` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tax_code` TEXT,"
    "  `tc_iss_date` TEXT,"
    "  `tc_exp_data` TEXT,"
    "  `name_in_vnese` TEXT,"
    "  `name_in_tran` TEXT,"
    "  `tax_reg_ad` TEXT,"
    "  `tel_num` TEXT,"
    "  `head_off_add` TEXT,"
    "  `tax_rec_add` TEXT,"
    "  `reg_cert_date` TEXT,"
    "  `reg_cert_num` TEXT,"
    "  `reg_cert_ad` TEXT,"
    "  `fin_year` TEXT,"
    "  `tax_reg_rec_date` TEXT,"
    "  `date_com_op` TEXT,"
    "  `chart_cap` TEXT,"
    "  `num_employee` TEXT,"
    "  `acc_model` TEXT,"
    "  `vat_cal_method` TEXT,"
    "  `own_name` TEXT,"
    "  `own_add` TEXT,"
    "  `dir_name` TEXT,"
    "  `dir_add` TEXT,"
    "  `chief_acc` TEXT,"
    "  `chief_acc_add` TEXT,"
    "  `main_busi_line` TEXT,"
    "  `paid_tax` TEXT,"
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
        out_json = item
        # start_id = item[1]
        print "File insert: ", out_json

        with open(out_json) as json_data:
            d = json.load(json_data)
            items = d['item']
            print len(items)
            # print len(items), " ", items[2336]['url']
            # print len(items), " ", items[2337]['url']
            for item in items:
                tax_code = addslashes(item['tax_code'])  # tax_code # Mã số ĐTNT
                tc_iss_date = addslashes(item['tc_iss_date'])  # tax_code_issue_date # Ngày cấp
                tc_exp_date = addslashes(item['tc_exp_date'])  # tax_code_expired_date # Ngày đóng MST
                name_in_vnese = addslashes(item['name_in_vnese'])  # name_in_vnese # Tên chính thức
                name_in_tran = addslashes(item['name_in_tran'])  # name_in_transaction # Tên giao dịch
                tax_reg_ad = addslashes(item['tax_reg_ad'])  # tax_registration_administrative # Nơi đăng ký quản lý
                tel_num = addslashes(item['tel_num'])  # telephone_number # Điện thoại
                head_off_add = addslashes(item['head_off_add'])  # head_office_address # Địa chỉ trụ sở
                tax_rec_add = addslashes(item['tax_rec_add'])  # tax_received_address # Địa chỉ nhận thông báo thuế
                reg_cert_date = addslashes(item['reg_cert_date'])  # enterprise_registration_certificate_date # QĐTL/Ngày cấp
                reg_cert_num = addslashes(item['reg_cert_num'])  # enterprise_registration_certificate_number # GPKD/Ngày cấp
                reg_cert_ad = addslashes(item['reg_cert_ad'])  # enterprise_registration_certificate_administrative # Cơ quan cấp
                fin_year = addslashes(item['fin_year'])  # finalcial_year']) # Năm tài chính
                tax_reg_rec_date = addslashes(item['tax_reg_rec_date'])  # tax_registration_form_received_date # Ngày nhận TK
                date_com_op = addslashes(item['date_com_op'])  # date_of_commencement_of_operation # Ngày bắt đầu HĐ
                chart_cap = addslashes(item['chart_cap'])  # charter_capital # Vốn điều lệ
                num_employee = addslashes(item['num_employee'])  # total_number_of_employee# Tổng số lao động
                acc_model = addslashes(item['acc_model'])  # accounting_model # Hình thức h.toán
                vat_cal_method = addslashes(item['vat_cal_method'])  # vat_calculation_method # PP tính thuế GTGT
                own_name = addslashes(item['own_name'])  # owner_name # Chủ sở hữu : Đỗ Văn Bắc
                own_add = addslashes(item['own_add'])  # owner_address # Địa chỉ chủ sở hữu
                dir_name = addslashes(item['dir_name'])  # director_name # Tên giám đốc
                dir_add = addslashes(item['dir_add'])  # director_address # Địa chỉ
                chief_acc = addslashes(item['chief_acc'])  # chief_accountant # Kế toán trưởng
                chief_acc_add = addslashes(item['chief_acc_add'])  # chief_accountant_address # Địa chỉ
                main_busi_line = addslashes(item['main_busi_line'])  # main_business_line # Ngành nghề chính
                paid_tax = addslashes(item['paid_tax'])  # paid_taxes'])  # Loại thuế phải nộp
                url = addslashes(item['url'])  # url # link chua thong tin cong ty
                # print tax_code, url, name_in_vnese
            #
            #     query = "INSERT INTO companies(id, name, address, legal_representative, issue_date, date_of_operation, tax_code, phone, url) " \
            #             "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (start_id, name, address, legal_representative, issue_date, date_of_operation, tax_code, phone, url)
            #     # print query
            #     cursor.execute(query)
            #     cnx.commit()
            #     start_id += 1

        print "Part 03 Done: ", out_json


    # cursor.close()
    # cnx.close()

    return 0

