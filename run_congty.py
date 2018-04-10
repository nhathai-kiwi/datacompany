
import congty_crawl as ctc
import os.path
import database_query as dbq
import urllib
import time
# crawl web: http://www.thongtincongty.com/
url_base = "http://www.thongtincongty.com/?page=%s"


# dinh dang file output
out_name_txt = 'congty%s.txt'
out_name_json = 'congty%s.json'


# duong dan cua cac folder
path = os.path.dirname(os.path.abspath(__file__))
save_path_txt = path.replace('/src', '/txt')
save_path_json = path.replace('/src', '/json')


# for i in range(13801, 18000, 100):
#     start_index = i
#     end_index = i + 99
#     # output file .txt gom url cua cac cong ty
#     number_index = end_index / 100
#     print "Iteration number: ", number_index
#
#     start_time = time.time()
#
#     name_of_file_txt = out_name_txt % (urllib.quote(str(number_index)))
#     complete_name_file_txt = os.path.join(save_path_txt, name_of_file_txt)  # congty%s.txt
#
#     ctc.print_link_txt(url_base, start_index, end_index, complete_name_file_txt)
#     elapsed_time = time.time() - start_time
#     print "Part 01 DONE, elapsed time: ", elapsed_time

out_json_files = []
a = [6, 12, 19, 21, 22, 23, 68, 74, 75, 77, 79, 80, 101, 103, 135, 138, 145, 149, 150, 159, 163]
for i in range(7701, 18000, 100):

    start_index = i
    end_index = i + 99
    # output file .txt gom url cua cac cong ty
    number_index = end_index / 100

    if a.count(number_index) == 1:
        continue
    # print "Iteration number: ", number_index

    #
    # name_of_file_txt = out_name_txt % (urllib.quote(str(number_index)))
    # complete_name_file_txt = os.path.join(save_path_txt, name_of_file_txt)  # congty%s.txt
    #
    # # doc url trong file txt va crawl lay thong tin tung cong ty ra file .json
    # name_of_file_json = out_name_json % (urllib.quote(str(number_index)))
    # complete_name_file_json = os.path.join(save_path_json, name_of_file_json)  # conty%s.json
    # print "file name: ", complete_name_file_json
    # start_time = time.time()
    # ctc.print_info_company_json(complete_name_file_txt, complete_name_file_json)
    # elapsed_time = time.time() - start_time
    # print "Part 02 DONE, elapsed time: ", elapsed_time
    #
    #

    # doc thong tin cong ty qua file json insert thong tin cong ty vao database

    name_of_file_json = out_name_json % (urllib.quote(str(number_index)))
    complete_name_file_json = os.path.join(save_path_json, name_of_file_json)  # conty%s.json
    start_id = (number_index - 1 )* 5000 + 1
    out_json_files.append( [complete_name_file_json, start_id] )

    #dbq.insert_company_from_json(complete_name_file_json, start_id)
    # elapsed_time = time.time() - start_time
    # print "Part 03 DONE, elapsed time: ", elapsed_time

    # print i, " ", complete_name_file_txt, " ", complete_name_file_json
# print out_json_files[0][0], " ", out_json_files[0][1]
# dbq.create_table()
dbq.insert_company_from_json(out_json_files)
# # miss congty 6,
