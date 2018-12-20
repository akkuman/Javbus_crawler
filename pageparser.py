#!/usr/bin/env python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import downloader
import re

def get_cili_url(soup):
    """get_cili(soup).get the ajax url and Referer url of request"""

    ajax_get_cili_url = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?lang=zh'
    ajax_data = soup.select('script')[8].text
    for l in ajax_data.split(';')[:-1]:
        ajax_get_cili_url += '&%s' % l[7:].replace("'","").replace(' ','')
    return ajax_get_cili_url


def get_size_in_MB(size_with_units):

    if 'GB' in size_with_units:
        size = int(float(size_with_units.replace('GB','')) * 1024)
    elif 'MB' in size_with_units:
        size = float(size_with_units.replace('MB',''))
    else:
        try:
            size = float(size_with_units)
            if size < 50:
                size = size * 1024
        except:
            size = 0;
    return int(size)


def resize_link_length(magnet_link):

    if len(magnet_link) < 255:
        return magnet_link
        
    return magnet_link.split("&dn")[0]

def parser_actor(actors):
    data = list()
    actors = (i.text.strip() for i in actors) if actors else ''
    for actor in actors:
        data.append(actor) 
    return data


def parser_magnet(html):

    soup = BeautifulSoup(html,"html.parser")
    data = list()

    magnet = {} # A dictionary

    for td in soup.select('td[width="70%"]'):
        # td.contents是它自己含的东西，再来一个.contents才是下一级的a
        # contents 偶数位置好像是navigator
        temp = magnet.copy()
        temp['Magnet_Name'] = td.contents[1].contents[0].strip() 
        temp['Magnet'] = resize_link_length(td.a['href'])
        temp['File_Size'] = get_size_in_MB(td.parent.contents[3].text.strip())
        temp['Share_Date'] = td.parent.contents[5].text.strip()

        data.append(temp)
    return data

def get_next_page_url(entrance, html):
    """get_next_page_url(entrance, html),return the url of next page if exist"""
    
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.select('a[id="next"]')
    if next_page:
        next_page_link = next_page[0]['href'].split('/')[-1:]
        next_page_link = '/'+'/'.join(next_page_link)
        next_page_url = entrance + next_page_link
        print("Next page is %s " % next_page_url)
        return next_page_url
    return None


def parser_homeurl(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html,"html.parser")
    for url in soup.select('a[class="movie-box"]'):
        yield url['href']


def parser_content(html):
    """parser_content(html),parser page's content of every url and yield the dict of content"""

    soup = BeautifulSoup(html, "html.parser")

    categories = {}
    
    code_name_doc = soup.find('span', text="識別碼:")
    code_name = code_name_doc.parent.contents[2].text if code_name_doc else ''
    categories['Video_ID'] = code_name

    date_issue_doc = soup.find('span', text="發行日期:")
    date_issue = date_issue_doc.parent.contents[1].strip() if date_issue_doc else ''
    categories['Release_Date'] = date_issue

    duration_doc = soup.find('span', text="長度:")
    duration = duration_doc.parent.contents[1].strip() if duration_doc else ''
    categories['Length'] = re.match(r"\d+", duration)[0]

    manufacturer_doc = soup.find('span', text="製作商:")
    manufacturer = manufacturer_doc.parent.contents[2].text if manufacturer_doc else ''
    categories['Producer'] = manufacturer

    series_doc = soup.find('span', text="系列:")
    series = series_doc.parent.contents[2].text if series_doc else ''
    categories['Series'] = series

    genre_doc = soup.find('p', text="類別:")
    genre =(i.text.strip() for i in genre_doc.find_next('p').select('span')) if genre_doc else ''
    genre_text = ''
    for tex in genre:
        genre_text += '%s   ' % tex 
    categories['Label'] = genre_text

    actors = soup.select('span[onmouseover^="hoverdiv"]')
    list_actor = parser_actor(actors)
    categories['Actors'] = list_actor

    url = soup.select('link[hreflang="zh"]')[0]['href']
    categories['URL'] = url

    magnet_html = downloader.get_html(get_cili_url(soup), Referer_url=url)
    magnet = parser_magnet(magnet_html)
    categories['Magnet'] = magnet

    # publisher_doc = soup.find('span', text="發行商:")
    # publisher = publisher_doc.parent.contents[2].text if publisher_doc else ''
    # categories['發行商'] = publisher

    # director_doc = soup.find('span', text="導演:")
    # director = director_doc.parent.contents[2].text if director_doc else ''
    # categories['導演'] = director

    return categories


