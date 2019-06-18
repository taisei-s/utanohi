# coding:utf-8

import urllib3
from bs4 import BeautifulSoup
import time
import re
from manager import CsvManager

def getArticleOfUtanohi(day, id_, pagename):
    """
    return parsed html on utanohi
    """
    url = f"http://utanohi.everyday.jp/{pagename}.php?no={day}{id_}"

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    time.sleep(5)

    soup = BeautifulSoup(r.data, 'html.parser')
    article = soup.main.article

    return article

def getTanka(article):
    tanka_tabs = []
    tanka_tabs += [article.find('a', class_="verse higher")]
    tanka_tabs += article.find_all('a', class_="verse other")

    tankas = []
    for tanka_tab in tanka_tabs:
        try:
            if tanka_tab.string is None:
                print(tanka_tab)
                tanka_tab.ruby.unwrap()
                tanka_tab.rt.extract()
                tanka_tab.rb.unwrap()

            tanka = tanka_tab.text.replace("\u3000", '  ')
            tankas.append(tanka)

        except:
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

        article = getArticleOfUtanohi(day, 's', 'index')

        for theme in article.find_all('a', class_="the"):
            themes.append(theme.strong.string)
            theme_link_id = theme.get("id")
            id_ = theme_link_id[0]
            article = getArticleOfUtanohi(day, id_, 'open')

            tankas.append(getTanka(article))
            print(theme.strong.string)

    for i in range(len(themes)):
        data.append([themes[i]] + tankas[i])

    print(data)

    return data


def main():
    days = 518
    csv_manager = CsvManager()
    data = getDataInUtanohi(days, first_day=518)
    #csv_manager.make_file(data, '../data/theme_tanka.csv')

if __name__ == "__main__":
    main()
