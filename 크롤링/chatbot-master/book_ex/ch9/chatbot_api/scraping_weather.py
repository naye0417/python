from bs4 import BeautifulSoup           # html, xml 분석도구
import urllib.request as req            # 웹 html/이미지 수집도구
import time
import schedule

def weather():
    # 네이버날씨
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8"
    html = req.urlopen(url)

    soup = BeautifulSoup(html, "html.parser")

    data1 = soup.find('div', {'class':'weather_box'})
    find_address = data1.find('span', {'class':'btn_select'}).text
    print('현재 위치: '+find_address)
    find_currenttemp = data1.find('span',{'class': 'todaytemp'}).text
    print('현재 온도: '+find_currenttemp+'℃')
    find_currentweather = data1.find('p',{'class': 'cast_txt'}).text
    print(find_currentweather)

    return find_address,find_currenttemp+'℃',find_currentweather


    # with open("날씨.txt", "w", encoding="utf-8") as f:
    #     f.write(find_address)
    #     f.write(",")
    #     f.write(find_currenttemp + '℃')
    #     f.write(",")
    #     f.write(find_currentweather)

    # find_text = data1.find('ul',{'class':'info_list'}).text
    # print('글자:'+ find_text)


#1시간마다 살생
# schedule.every().hour.do(weather)
#
#
# while True:
#     schedule.run_pending()
#     time.sleep(1);