
import congty_crawl as ctc
import os.path
import time
import doanhnghiep_crawl as dnc
import doanhnghiep_db_query as ddq

# duong dan cac folder
path = os.path.dirname(os.path.abspath(__file__))
save_path_txt = path.replace('/src', '/txt/doanhnghiep')
save_path_json = path.replace('/src', '/json/doanhnghiep')

ttdn_xlsx = 'ttdn.xlsx'
num_pattern_url = 562
# read_url_company_from_xlsx(ttdn.xlsx,2, 3, 563)
# doc url pattern tu file ttdn.xlsx
url_bases, num_page = dnc.read_url_company_from_xlsx(inp_xlsx=ttdn_xlsx, col_index_url=2, col_index_page=3, num_row=563)


# for i in range(0, 562):
#     print url_bases[i], " ", num_page[i], type(num_page[i]), i, dnc.convert_format_int(i)

for i in range(288, num_pattern_url):
    pattern_index = i + 1
    print "Start pattern number: ", pattern_index

    # # Part 01: write url into .txt file
    # start_time = time.time()
    #
    # url_pattern = url_bases[i] + '?p=%s'
    #
    name_of_file_txt = dnc.convert_format_int(pattern_index) + '.txt'
    complete_name_file_txt = os.path.join(save_path_txt, name_of_file_txt)
    print complete_name_file_txt
    # # print complete_name_file_txt, " ", min(1000, num_page[i])
    # dnc.print_link_txt(url_pattern, 1, min(1000, num_page[i]), complete_name_file_txt)

    # elapsed_time = time.time() - start_time
    # print "Part 01 DONE, elapsed time: ", elapsed_time
    #
    # Part 02: generate company info and write into .json file
    start_time = time.time()

    name_of_file_json = dnc.convert_format_int(pattern_index) + '.json'
    complete_name_file_json = os.path.join(save_path_json, name_of_file_json)
    print complete_name_file_json
    dnc.print_info_company_json(complete_name_file_txt, complete_name_file_json)
    #
    # elapsed_time = time.time() - start_time
    # print "Part 02 DONE, elapsed time: ", elapsed_time
    #

    # Part 2 stop tai pattern number 47