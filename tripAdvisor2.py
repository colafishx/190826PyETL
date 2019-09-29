from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import json

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def isAlpha(word):
    try:
        return word.encode('ascii').isalpha()
    except UnicodeEncodeError:
        return False

df = pd.DataFrame(columns=["中文", "英文", "評分","標籤", "排名","地址","評論"])


n=0
try:
    url = "https://www.tripadvisor.com.tw/Attractions-g298184-Activities-Tokyo_Tokyo_Prefecture_Kanto.html"
    response = urlopen(url)
    html = BeautifulSoup(response)
    total = []
    for t in html.find_all("li", class_="attractions-attraction-overview-pois-PoiCard__item--3UzYK"):
        if not t.find("a") == None:
            turl = "https://www.tripadvisor.com.tw" + t.find("a")["href"]
            total.append(turl)
    print(total)

    for x in total:
        url1 = x
        response = urlopen(url1)
        html = BeautifulSoup(response)

        ch = html.find(class_="ui_header h1")
        rating = html.find(class_="ui_bubble_rating")
        type = html.find("div", class_="detail")
        rank = html.find(class_="header_popularity")
        address = html.find("span", class_="detail")
        title_ch = ''
        title_en = ''

        # print("---------------------------")
        if isAlpha(ch.text.split(' ')[1]):
            # print(ch.text.split(' ')[1])
            title_ch = None
            # print(title_ch)
            title_en = ' '.join(ch.text.split(' ')[1:])
            title_name = title_en
        else:
            title_ch = ch.text.split(' ')[1]
            title_en = (' '.join(ch.text.split(' ')[2:]))
            title_name = title_ch

        print(title_ch)
        print(title_en)

        # Comment
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        # import the webdriver
        driver = webdriver.Chrome("./chromedriver", options=options)
        driver.get(url1)

        num = 0
        comment = []
        try:
            end_page = driver.find_element_by_class_name("pageNumbers").find_element_by_class_name("last").text
            print(end_page)
        except:
            print("一頁而已")
            end_page = 1

        for i in range(int(end_page)):
            url2 = url1.split("-")[0] + "-or" + str(num) + "-" + '-'.join(url1.split("-")[1:])
            # print(url2)
            try:
                driver.get(url2)
                time.sleep(2)
                if (check_exists_by_xpath("//span[@class='taLnk ulBlueLinks']")):
                    # 找到"更多"的按鍵
                    for item in driver.find_elements_by_class_name(
                            'taLnk ulBlueLinks'):  # driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']"):
                        item.click()
                        time.sleep(4)

                container = driver.find_elements_by_xpath("//div[@class='review-container']")

                for j in container:
                    comment.append(j.text.split('\n')[5:7])


            except:
                print("重跑")
                # break
            num += 10
        driver.close()

        data = {"中文": title_ch,
                "英文": title_en,
                "標籤": type.text,
                "評分": rating["alt"],
                "排名": rank.text,
                "地址": address.text,
                "內文": comment}
        df = df.append(data, ignore_index=True)
    #df.to_csv("第1頁.csv", encoding="utf-8", index=False)
    # 存資料
        number = 1
        dn = "tripadvisor/" + title_name
        if not os.path.exists(dn):
            os.makedirs(dn)
        f = open(dn + "/" + str(number) + "_" + title_name + ".json", "w", encoding="utf-8")
        json.dump(data, f)
        f.close()
        number+=1
except:
    #df.to_csv("第1頁.csv", encoding="utf-8", index=False)
    # 存資料
    number = 1
    dn = "tripadvisor190921/" + title_name
    if not os.path.exists(dn):
        os.makedirs(dn)
    f = open(dn + "/" + str(number) + "_" + title_name + ".json", "w", encoding="utf-8")
    json.dump(data, f)
    f.close()
        # #with open('tourist1.csv','a',encoding="utf-8"):
        # """
        # row = df
        # with open('tourist1.csv', 'a') as csvFile:
        #     writer = csv.writer(csvFile)
        #     writer.writerow(row)
        # csvFile.close()
        # """


print("*" * 50)
