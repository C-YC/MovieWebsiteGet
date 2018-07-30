# -*- coding:utf-8 -*-
"""
author:C-YC
target:爬取不同网址07～18年所有电影的年份、名字、url、电影id
finish date：2018,07,
"""
import sys
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
reload(sys)
sys.setdefaultencoding("utf-8")
browser = webdriver.PhantomJS(executable_path="./phantomjs")

# row = {}
# row['movie_year'] = year
# row['movie_name'] = movie_name
# row['movie_url'] = movie_url
# row['movie_id'] = movie_id
# movie_list.append(row)
# movie_info = pd.DataFrame(movie_list)
# time.sleep(1)
# movie_info.to_csv("../movie_sites/" + movie_site + "/movie_" + str(year) + ".csv", index=False, sep=',')

# with open("../movie_sites/1905电影网/crawled_year.txt", "r")as f:
#     lines = f.readlines()
#     print len(lines)
#     print lines[-1]
    # year = lines[-1].split("`")[0]
    # total_pages = lines[-1].split("`")[1]
    # page = lines[-1].split("`")[2].replace("\n", "")
    # print year, total_pages, page

year_1 = '2007'
year_2 = '2008'
year_3 = '2009'
name_1 = 'qwe'
name_2 = 'asd'
name_3 = 'zxc'
name_list = []
name_list.append(year_1)
name_list.append(name_1)
name_list.append(year_2)
name_list.append(name_2)
name_list.append(year_3)
name_list.append(name_3)
print name_list

flag = 0
for r in range(3):
    if r / 3 == 1:
        flag = 1
    else:
        pass
if flag == 1:
    print "yes!!"
else:
    print "no!!!"

a = set('abc')
b = set(['a', 'p', 'b'])
c = set('abcdgp')
ret = c - (a | b)
print ret


page_url = 'http://movie.mtime.com/movie/search/section/#year=2010&pageIndex=242'
browser.get(page_url)
movie_list = []
movies = browser.find_elements_by_xpath("//ul[@class='ser_mlist2']//h3[@class='normal mt6']")
print len(movies)
for movie in movies:
    year = '2010'
    print year,
    time.sleep(0.2)
    movie_name = movie.find_element_by_xpath("a").text
    if len(movie_name) > 0:
        print movie_name,
        movie_url = movie.find_element_by_xpath("a").get_attribute("href")
        print movie_url,
        movie_id = movie_url.split("com/")[1].replace("/", "")
        print movie_id
        time.sleep(0.2)
        movie_list.append(year)
        movie_list.append(movie_name)
        movie_list.append(movie_url)
        movie_list.append(movie_id)
    else:
        print "movie name does not exist！"
        pass
print movie_list