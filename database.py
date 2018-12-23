#!/usr/bin/env python
#-*-coding:utf-8-*-

import pymysql.cursors
import re

connection = pymysql.connect(host='47.254.83.13', user='javbus', password='whywhy', db='javbus', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def write_data(dict_jav, censored):
    
    # Video
    with connection.cursor() as cursor:
        try:
            # sql_video = "INSERT INTO `Video` (`Video_ID`, `URL`, `Release_Date`, `Length`, `Producer`, `Series`, `Label`, `Censored`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            # cursor.execute(sql_video, (dict_jav['Video_ID'], dict_jav['URL'], dict_jav['Release_Date'], dict_jav['Length'], dict_jav['Producer'], dict_jav['Series'], dict_jav['Label'], int(censored)))
            sql_video = "INSERT INTO `Video` (`Video_ID`, `URL`, `Release_Date`, `Length`, `Producer`, `Series`, `Label`, `Censored`) SELECT %s,%s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT `Video_ID` FROM `Video` WHERE `Video_ID` = %s);"
            cursor.execute(sql_video, (dict_jav['Video_ID'], dict_jav['URL'], dict_jav['Release_Date'], dict_jav['Length'], dict_jav['Producer'], dict_jav['Series'], dict_jav['Label'], int(censored), dict_jav['Video_ID']))
        except Exception as e:
            print(e)
            print("Failed Video %s" % dict_jav['Video_ID'])
            with open('fail.txt', 'a') as fd:
                fd.write('%s\n' % e)
                fd.write('%s\n\n\n' % dict_jav['Video_ID'])
            

    # Magnet
    with connection.cursor() as cursor:
        for magnet in dict_jav['Magnet']:
            try:
                # sql_magnet = "INSERT INTO `Magnet` (`Hash`, `Magnet`, `Video_ID`, `File_Size`, `Share_Date`, `Magnet_Name`, `Source`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                # cursor.execute(sql_magnet, (get_hash(magnet['Magnet']), magnet['Magnet'], dict_jav['Video_ID'], magnet['File_Size'], magnet['Share_Date'], magnet['Magnet_Name'], 'Javbus'))
                sql_magnet = "INSERT INTO `Magnet` (`Hash`, `Magnet`, `Video_ID`, `File_Size`, `Share_Date`, `Magnet_Name`, `Source`) SELECT %s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT `Hash` FROM `Magnet` WHERE `Hash` = %s);"
                cursor.execute(sql_magnet, (get_hash(magnet['Magnet']), magnet['Magnet'], dict_jav['Video_ID'], magnet['File_Size'], magnet['Share_Date'], magnet['Magnet_Name'], 'Javbus', get_hash(magnet['Magnet'])))
            except Exception as e:
                print(e)
                print("Failed Magnet %s" % magnet['Magnet'])
                with open('fail.txt', 'a') as fd:
                    fd.write('%s\n' % e)
                    fd.write('%s\n' % dict_jav['Video_ID'])
                    fd.write('%s\n\n\n' % magnet['Magnet'])
                continue

    # Actor
    with connection.cursor() as cursor:
        for actor in dict_jav['Actors']:
            try:
                sql_actor = "INSERT INTO `Actor` (`name`) SELECT %s WHERE NOT EXISTS (SELECT `name` FROM `Actor` WHERE `name` = %s);"
                sql_video_actor = "INSERT INTO `Video_Actor`(`Video_ID`, `Actor`) SELECT %s, %s WHERE NOT EXISTS (SELECT `Video_ID`, `Actor` FROM `Video_Actor` WHERE `Video_ID` = %s AND `Actor` = %s);"
                cursor.execute(sql_actor, (actor, actor))
                cursor.execute(sql_video_actor, (dict_jav['Video_ID'], actor, dict_jav['Video_ID'], actor))

            except Exception as e:
                print(e)
                print("Failed Actor %s Video %s" % (actor, dict_jav['Video_ID']))
                with open('fail.txt', 'a') as fd:
                    fd.write('%s\n' % e)
                    fd.write('%s\n' % actor)
                    fd.write('%s\n\n\n' % dict_jav['Video_ID'])
                continue

    connection.commit()

def pick_one_actor():
    with connection.cursor() as cursor:
        try:
            sql_select = "SELECT `name` FROM `Actor` WHERE `iteration_started` = 0 LIMIT 1"
            cursor.execute(sql_select)
            result = cursor.fetchall()
            if not result:
                return
            sql_update = "UPDATE `Actor` SET `iteration_started` = 1 WHERE `name` = %s"
            cursor.execute(sql_update, result[0]['name'])

        except Exception as e:
            print(e)
    connection.commit()
    return result[0]['name']

def set_iterated(name):
    with connection.cursor() as cursor:
        try:
            sql_update = "UPDATE `Actor` SET `iterated` = 1 WHERE `name` = %s"
            cursor.execute(sql_update, name)
        except Exception as e:
            print(e)
    connection.commit()

def get_hash(magnet):
    regex = r"[a-fA-F\d]{40}"
    torrent_hash = re.search(regex, magnet)
    return torrent_hash.group()

def check_url_not_in_table(url):
    with connection.cursor() as cursor:

        sql = "SELECT `URL` FROM `Video` WHERE `URL`= %s"
        cursor.execute(sql, url)
        # cursor.execute(sql, (url,))
        result = cursor.fetchone()
    if result:
        return False
    return True
