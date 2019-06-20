# coding:utf-8

import urllib3
from bs4 import BeautifulSoup
import html5lib
import time
import re
from manager import CsvManager, JsonManager, TxtManager

def getArticleOfUtanohi(day, id_, pagename):
    """
    return parsed html on utanohi
    """
    url = f"http://utanohi.everyday.jp/{pagename}.php?no={day}{id_}"

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    time.sleep(5)

    soup = BeautifulSoup(r.data, 'html5lib')
    article = soup.main.article

    return article

def getTanka(article):
    tanka_tabs = article.find_all('a', class_=re.compile(r'^verse'))

    tankas = []
    for tanka_tab in tanka_tabs:
        try:
            if tanka_tab.string is None:
                tanka_tab.ruby.unwrap()
                tanka_tab.rt.extract()
                tanka_tab.rb.unwrap()

            tanka = tanka_tab.text.replace("\u3000", '  ')
            tankas.append(tanka)
        except AttributeError:
            continue

    return tankas


def getDataInUtanohi(days, first_day=1):

    data = []
    tankas = []
    themes = []
    love = []
    like = []

    for day in range(first_day, days+1):

        print(day)

        article_day = getArticleOfUtanohi(day, 's', 'index')

        for theme in article_day.find_all('a', class_="the"):
            themes.append(theme.strong.string)
            theme_link_id = theme.get("id")
            id_ = theme_link_id[0]
            article_theme = getArticleOfUtanohi(day, id_, 'open')

            tankas.append(getTanka(article_theme))

    for i in range(len(themes)):
        data.append([themes[i]] + tankas[i])

    return data

def getAllTanka():
    #437, 518, 978
    today = 1904
    data = getDataInUtanohi(365)
    csv_manager = CsvManager()
    csv_manager.make_file(data, '../data/theme_tanka.csv')

    for day in range(366, today, 365):
        last_day = day + 365 - 1
        if last_day > today:
            last_day = today
        data = getDataInUtanohi(last_day, first_day=day)
        csv_manager.add_file(data, '../data/theme_tanka.csv')


def main():
    getAllTanka()

if __name__ == "__main__":
    main()
