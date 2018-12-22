#!/usr/bin/env python
#-*-coding:utf-8-*-

import database
import downloader
import pageparser
import time

def get_dict(url):
    """get the dict of the detail page and yield the dict"""

    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        detail_page_html = downloader.get_html(detail_url)
        dict_jav = pageparser.parser_content(detail_page_html)
        #重写url
        dict_jav['URL'] = detail_url
        yield dict_jav, detail_url


def page_crawler(url,is_censored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if database.check_url_not_in_table(detail_url):
            # print("%s is going to be written" % detail_url)

            database.write_data(dict_jav_data, is_censored)
            print("Crawled %s" % detail_url)
        else:
            # database.write_data(dict_jav_data, is_censored)
            print("Done with %s " % detail_url)
            # time.sleep(60)
            # exit()



def main(entrance):
    #无码为1，有码为0
    is_censored = 0 if 'uncensored' in entrance else 1
    
    page_crawler(entrance, is_censored)  
    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)

    while next_page_url:
        page_crawler(next_page_url,is_censored)
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)

def actor_iterator():
    while True:
        name = database.pick_one_actor()
        if not name:
            return
        print("Crawling %s's video" % name)
        main('https://www.javbus.com/search/' + name)
        main('https://www.javbus.com/uncensored/search/' + name)
        database.set_iterated(name)

def list_iterator():
    file = open("id.txt")
    while 1:
        line = file.readline()
        if not line:
            break
        main('https://www.javbus.com/search/' + line.strip())
        # main('https://www.javbus.com/uncensored/search/' + line)


if __name__ == '__main__':
    # actor_iterator()
    list_iterator()
    # main('https://www.javbus.com/search/ASUKA/8')
    # main('https://www.javbus.com/search/')


