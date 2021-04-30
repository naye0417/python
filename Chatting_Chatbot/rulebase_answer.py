from bs4 import BeautifulSoup
import urllib.request as req
import requests
from selenium import webdriver
import os
import time
from selenium.webdriver.chrome.options import Options
import json
import json
import re


from konlpy.tag import Twitter
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc

import pytagcloud
import webbrowser

from matplotlib.image import imread

def showGraph(wordInfo, filename):
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    matplotlib.rc("font", family=font_name)

    plt.xlabel("main_keyword")
    plt.ylabel("frequency")
    plt.grid(True)

    Sorted_Dict_Values = sorted(wordInfo.values(), reverse=True)
    Sorted_Dict_Keys = sorted(wordInfo, key=wordInfo.get, reverse=True)

    plt.bar(range(len(wordInfo)), Sorted_Dict_Values, align="center")
    plt.xticks(range(len(wordInfo)), list(Sorted_Dict_Keys), rotation="70")

    plt.savefig(filename)
    webbrowser.open(filename)
    # plt.show()

def saveWordCloud(wordInfo, filename):
    time.sleep(3)
    taglist = pytagcloud.make_tags(dict(wordInfo).items(), maxsize=70)
    pytagcloud.create_tag_image(taglist, filename, size=(1200, 1024), fontname="korean", rectangular=False)

    # img = imread(filename)
    # plt.imshow(img)
    # plt.show()
    webbrowser.open(filename)

def answer_analysis_naver():
    message = answer_naver_news()
    message = message.replace("<br />", "")
    message = message.replace("<br>", "")


    message = re.sub(r'[^\w]', ' ', message) + ' '

    nlp = Twitter()
    nouns = nlp.nouns(message)
    count = Counter(nouns)

    ret_data = ""
    wordInfo = dict()
    for tags, counts in count.most_common(15):
        if (len(str(tags)) > 1):
            wordInfo[tags] = counts
            print("%s : %d" % (tags, counts))
            ret_data += "%s : %d <br>" % (tags, counts)

    return wordInfo, ret_data


def trans_json(query, answer, answer_image="", intent_name="", ner_predicts=""):
    send_json_data_str = {
        "Query": query,
        "Answer": answer,
        "AnswerImageUrl": answer_image,
        "Intent": intent_name,
        "NER": str(ner_predicts)
    }

    message = json.loads(json.dumps(send_json_data_str))
    return message

def answer_weather():
    url = "http://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108"

    # 데이터 가져오기
    res = req.urlopen(url)
    # html = res.read().decode("utf-8")     # 문자열 가져오기
    # print(html)

    # html 분석하기
    soup = BeautifulSoup(res, 'html.parser')  # XML도 html.parser로 해도 됨
    # soup = BeautifulSoup(html, 'html.parser')

    # title과 wf를 추출하기
    title = soup.find("title").string  # 태그사이의 문자열 추출
    wf = soup.find("wf").string
    wf = wf.replace("○", "")  # ○ 을 지우기
    # wf = wf.replace("<br />", "\n")  # <br /> => 개행문자로 변환
    print("[{}]\n{}".format(title, wf))

    return "[{}]<br>{}".format(title, wf)

def answer_naver_news():
    url = "https://news.naver.com/"
    # 스크레이핑 App이 아닌 브라우저로 접근하는 것처럼 해주는 헤더설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    html = requests.get(url, headers=headers).text

    bs = BeautifulSoup(html, 'html.parser')

    headline = bs.find("ul", {"class": "hdline_article_list"})
    a_news = headline.find_all("a", {"class": "lnk_hdline_article"})
    for a in a_news:
        print("headline: ", a.text.strip())

    etc_uls = bs.find_all("ul", {"class": "mlist2 no_bg"})
    ret_data = ""
    for ul in etc_uls:
        news = ul.find_all("strong")
        for i, n in enumerate(news):
            print("news: ", n.text)
            ret_data += "{} {}".format(i, n.text)
            ret_data += '<br>'

    return ret_data


def answer_naver_movie_ranking():
    url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"

    res = req.urlopen(url)

    soup = BeautifulSoup(res, 'html.parser')

    movie_li = soup.select("#old_content > table > tbody > tr > td.title > div > a")
    ret_data = ""
    for i, movie in enumerate(movie_li):
        print("{}:{}".format(i + 1, movie.text))
        ret_data += "{}:{}".format(i + 1, movie.text)
        ret_data += '<br>'

    return ret_data

def answer_naver_site():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.naver.com")


def answer_daum_site():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.daum.net")


