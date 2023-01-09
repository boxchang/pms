#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import os
import datetime
now = datetime.datetime.now()
file_name = datetime.datetime.strftime(now,'%Y%m%d %H%M%S')
delete_keyword = datetime.datetime.strftime((now - datetime.timedelta(days = 3)), '%Y%m%d')
print(delete_keyword)
print(file_name)

print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
src = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'db.sqlite3')

dst_path = 'C:\\Users\\hsiangchih.chang\\Desktop\\Temp\\'
dst = dst_path + file_name + ".sqlite3"

for dirpath, dirName, filenames in os.walk(dst_path):
    for file in filenames:
        if "20230106" in file:
            print(file)
            os.remove(dst_path+file)


# print(src)
# result = os.path.isfile(src)
# if result:
#     shutil.copyfile(src, dst)
# print(result)

# src = 'C:\\Users\\hsiangchih.chang\\Desktop\\Temp\\Invoice.pdf'
# dst = 'C:\\Users\\hsiangchih.chang\\Desktop\\Temp\\Invoice2.pdf'
# shutil.copyfile(src, dst)
