#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3
import pymysql.cursors
import re

connection = pymysql.connect(host='47.254.83.13',
                             user='javbus',
                             password='whywhy',
                             db='javbus',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



def write_data(dict_jav, censored):

    # dict_jav['URL'], 
    # dict_jav['識別碼'], 
    # dict_jav['發行日期'], 
    # dict_jav['長度'], 
    # dict_jav['導演'], 
    # dict_jav['製作商'], 
    # dict_jav['發行商'], 
    # dict_jav['系列'], 
    # dict_jav['演員'], 
    # dict_jav['類別'], 
    # dict_jav['磁力链接']
    # censored
    
    with connection.cursor() as cursor:
        # Create a new record
        sql_video = "INSERT INTO `Video` (`Video_ID`, `URL`, `Release_Date`, `Idol`, `Length`, `Studio`, `Producer`, `Lable`, `Censored`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_video, (dict_jav['識別碼'], dict_jav['URL'], dict_jav['發行日期'],dict_jav['演員'], dict_jav['長度'], dict_jav['製作商'], dict_jav['發行商'], dict_jav['類別'], int(censored)))

    
    with connection.cursor() as cursor:
        for magnet in dict_jav['磁力链接']:
            try:
                sql_magnet = "INSERT INTO `Magnet` (`Magnet`, `Video_ID`, `File_Size`, `Share_Date`, `Magnet_Name`) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql_magnet, (magnet['Magnet'], dict_jav['識別碼'], magnet['File_Size'], magnet['Share_Date'], magnet['Magnet_Name'] ))
                # print(magnet)
            except:
                with open('fail_url.txt', 'a') as fd:
                    fd.write('%s\n' % magnet['Magnet'])
                print("Fail to write %s" % magnet['Magnet'])
                continue
    

    connection.commit()


def check_url_not_in_table(url):
    with connection.cursor() as cursor:

        sql = "SELECT `URL` FROM `Video` WHERE `URL`= %s"
        cursor.execute(sql, (url,))
        result = cursor.fetchone()
    if result:
        return False
    return True