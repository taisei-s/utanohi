# coding:utf-8

import urllib3
from bs4 import BeautifulSoup
import html5lib
import time
import re
from manager import CsvManager, JsonManager, TxtManager
import dynamodb
import boto3

def getArticleOfUtanohi(day, id_, pagename):
    """
    return parsed html on utanohi
    """
    url = f"http://utanohi.everyday.jp/{pagename}.php?no={day}{id_}"

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    time.sleep(5)

    soup = BeautifulSoup(r.data, 'html5lib')
    article = soup.main.find('article', id="hall")

    return article

def getAuthor(section):
    author = section.find('a', class_="name")

    if author.text == '':
        return None
    else:
        return author.text

def getTanka(section):
    tanka = section.find('a', class_=re.compile(r'^verse'))

    tanka_pattern = re.compile(r'<a class=".+?">(.*?)</a>')
    tanka = tanka_pattern.findall(str(tanka))
    tanka = tanka[0].replace("\u3000", '  ')

    if tanka == '':
        return None
    else:
        return tanka

def getLove(section):
    love = section.find('b', class_='love red')
    love = re.match(r'^[0-9]', love.text)

    if love == None or love[0] == '':
        return None
    else:
        return int(love[0])

def getLike(section):
    like = section.find('b', class_='like fuchsia')

    if like == None or like.text == '':
        return None
    else:
        return int(like.text)

def getTankaInfo(article):
    sections = article.find_all('section', class_='per mrz')

    tanka_info = []
    for section in sections:
        info = {
            'Author': getAuthor(section),
            'tanka': getTanka(section),
            'love': getLove(section),
            'like': getLike(section)
        }
        tanka_info.append(info)

    return tanka_info

def getTotalPoint(article):
    section = article.find('section', id="loin")
    p = section.find('p', class_="number cnt fs12 yellow nobr in2")
    total_point = p.find('b', class_="base fs12")

    return int(total_point.text)

def getTankaNum(article):
    section = article.find('section', id="loin")
    p = section.find('p', class_="number cnt fs12 fuchsia nobr in1")
    tanka_num = p.find('b', class_="base fs12")

    return int(tanka_num.text)

def getDataInUtanohi(day):

    data = []

    print(day)

    article_day = getArticleOfUtanohi(day, 's', 'index')

    for theme in article_day.find_all('a', class_="the"):
        theme_link_id = theme.get("id")
        try:
            theme = theme.strong.text
        except AttributeError:
            continue
        id_ = theme_link_id[0]
        theme_id = str(day) + id_
        article_theme = getArticleOfUtanohi(day, id_, 'open')

        item = {
            'theme': theme,
            'theme_id': theme_id,
            'tanka_num': getTankaNum(article_theme),
            'total_point': getTotalPoint(article_theme),
            'tanka_info': getTankaInfo(article_theme)
        }
        data.append(item)

    return data

def getAllTanka(today, first_day=1):
    #tableName = 'utanohi'
    tableName = 'testTable'
    myDynamodb = boto3.resource(
        'dynamodb',
        region_name='ap-northeast-1',
        endpoint_url='http://localhost:8000',
        aws_access_key_id='ACCESS_ID',
        aws_secret_access_key='ACCESS_KEY')
    table = myDynamodb.Table(tableName)

    for day in range(first_day, today):
        data = getDataInUtanohi(day)
        dynamodb.batch_write(table, data)

def main():
    #437, 518, 978,1572, 1587, 1588, 1820
    today = 1923
    #getAllTanka(today)
    getAllTanka(1573, first_day=1572)
    #data = getDataInUtanohi(1913)
    #for d in data:
    #    print(d)


if __name__ == "__main__":
    main()
