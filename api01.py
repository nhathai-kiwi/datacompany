#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time
import os
import openpyxl


# get all link company
def get_all_url_companys(url_base, start, end):
    print "url_base: ", url_base
    links = []
    for i in range(start, end + 1):
        len_page = 0
        while len_page < 1000:
            print "Page number: ", i
            url = url_base % (urllib.quote(str(i)))
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            # print "Len data: ", len(data)
            len_page = len(data)
            for company in soup.find_all('div', attrs={'class': "news-v3 bg-color-white"}):
                link = company.find('a')
                url = 'https://thongtindoanhnghiep.co' + link.get('href')
                links.append(url)
                # print "Link: ", url

    return links
# DONE


def get_info_city(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    # print soup.text
    len_page = len(data)

    print "Len page: ", len_page # 7845
    decoded = json.loads(soup.text)
    print len(decoded['LtsItem'])
    f = open("city.txt", "w")

    num_city = len(decoded['LtsItem'])
    for city in decoded['LtsItem']:
        # print city
        f.write(str(city['ID'])  + " "+ str(city['TotalDoanhNghiep']) + " " + str(city['SolrID']) + " " + str(city['Title']) + "\n")

def get_info_dis(url_dis_base):
    # url_dis_base = 'https://thongtindoanhnghiep.co/api/city/%s/district'
    f = open("district.txt", "w")
    for i in range(1, 64):
        url = url_dis_base % (urllib.quote(str(i)))
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        # print soup.text
        len_page = len(data)

        print "Url: ", url, " Len page: ", len_page # 7845

        decoded = json.loads(soup.text)
        for district in decoded:
            f.write(str(district["SolrID"]) + " " + str(district["ID"]) + " " + str(district["Title"]) + "\n" )

def get_info_ward(district_txt, url_ward_base):

    answer = 0

    fw = open("ward.txt", "a")
    fr = open(district_txt, "r")
    cnt = 0
    for line in fr:
        cnt += 1
        dis = line.split(' ')
        url = url_ward_base % (urllib.quote(str(dis[1])))
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')
        len_page = len(soup.text)

        print "number: ", cnt, "Url: ", url, " Len page: ", len_page  # 7845

        try:
            json_decoded = json.loads(soup.text)
        except ValueError, e:
            pass  # invalid json
        else:
            pass  # valid json

            answer += len(json_decoded)
            for ward in json_decoded:
                fw.write(str(ward["SolrID"]) + " " + str(ward["ID"]) + " " + str(ward["Title"]) + "\n")
                # print str(ward["SolrID"]) + " " + str(ward["ID"]) + " " + str(ward["Title"]) + "\n"
            print "Done url: ", url

    return answer


def get_info_w(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    # print soup.text

    len_page = len(data)

    print "Url: ", url, " Len page: ", len_page  # 7845
    try:
        json_decoded = json.loads(soup.text)
    except ValueError, e:
        pass  # invalid json
    else:
        pass  # valid json

        print len(json_decoded)
        for ward in json_decoded:
            # fw.write(str(ward["SolrID"]) + " " + str(ward["ID"]) + " " + str(ward["Title"]) + "\n")
            print str(ward["SolrID"]) + " " + str(ward["ID"]) + " " + str(ward["Title"]) + "\n"


# url_city = 'https://thongtindoanhnghiep.co/api/city'
# get_info_city(url_city)
#
#
# url_dis_base = 'https://thongtindoanhnghiep.co/api/city/%s/district'
# get_info_dis(url_dis_base)

url_ward_base = 'https://thongtindoanhnghiep.co/api/district/%s/ward'
district_txt = 'district.txt'
get_info_ward(district_txt, url_ward_base)

# get_info_w('https://thongtindoanhnghiep.co/api/district/745/ward')

def test_url_json(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data
