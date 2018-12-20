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
        # try:
            detail_page_html = downloader.get_html(detail_url)
            dict_jav = pageparser.parser_content(detail_page_html)
            #重写url
            dict_jav['URL'] = detail_url
        # except:
        #     with open('fail_url.txt', 'a') as fd:
        #         fd.write('%s\n' % detail_url)
        #     print("Fail to crawl %s\ncrawl next detail page......" % detail_url)
        #     continue
            yield dict_jav, detail_url


def join_db(url,is_censored):
    """the detail_dict of the url join the db"""

    for dict_jav_data, detail_url in get_dict(url):
        if controler.check_url_not_in_table(detail_url):
            # print("%s is going to be written" % detail_url)

            controler.write_data(dict_jav_data, is_censored)
            print("Crawled %s" % detail_url)
        else:
            print("%s is done" % detail_url)
            # time.sleep(60)
            # exit()



def main(entrance):
    #无码为1，有码为0
    is_censored = 0 if 'uncensored' in entrance else 1
    join_db(entrance, is_censored)
    
    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url,is_censored)
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        if next_page_url == None:
            break


if __name__ == '__main__':
    main('https://www.javbus.com/page')
    # main('https://www.javbus.com/uncensored/search/-')
    # main('https://www.javbus.com/search/')


