#!/usr/bin/env python
#-*-coding:utf-8-*-

import controler
import downloader
import pageparser
import time

def get_dict(url):
    """get the dict of the detail page and yield the dict"""

    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        try:
            detail_page_html = downloader.get_html(detail_url)
            dict_jav = pageparser.parser_content(detail_page_html)
        except:
            with open('fail_url.txt', 'a') as fd:
                fd.write('%s\n' % detail_url)
            print("Fail to crawl %s\ncrawl next detail page......" % detail_url)
            continue
        yield dict_jav, detail_url


def join_db(url,is_uncensored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if controler.check_url_not_in_table(url):
            controler.write_data(dict_jav_data, is_uncensored)
            print("Crawled %s" % detail_url)
        else:
            print("it has updated over...window will be closed after 60s")
            time.sleep(60)
            exit()



def main(entrance):
    #创建数据表
    controler.create_db()
    #无码为1，有码为0
    is_uncensored = 1 if 'uncensored' in entrance else 0
    join_db(entrance, is_uncensored)

    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url,is_uncensored)
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        if next_page_url == None:
            break


if __name__ == '__main__':
    main('https://www.javbus5.com')
    main('https://www.javbus5.com/uncensored')