# -*- coding:utf-8 -*-
"""
author:C-YC
target:爬取中国票房网、豆瓣网和中国排片数据库07～18年电影的名字、链接、id，并存入redis中
finish date：2018,07,29
"""
import sys
import time
import login
import json
import connect_redis
import os
import urllib
import urllib2
import restart_58921
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
reload(sys)
sys.setdefaultencoding("utf-8")
browser = webdriver.Firefox(executable_path="./geckodriver")


def __cbooo_get(movie_site):
    browser.get("http://www.cbooo.cn/movies")
    time.sleep(1)
    with open("../movie_sites/"+movie_site+"/crawled_year.txt", "r")as f:
        lines = f.readlines()
    if len(lines) > 0:
        crawling_year = lines[-1].split("`")[0]
        total_page = lines[-1].split("`")[1]
        crawling_page = lines[-1].split("`")[2].replace("\n", "")
        print crawling_year, total_page, crawling_page
    else:
        crawling_year = '2007'
        total_page = '-1'
        crawling_page = '0'
        print crawling_year, total_page, crawling_page
    if total_page != crawling_page:
        movie_year = int(crawling_year)
    else:
        movie_year = int(crawling_year)+1
        crawling_page = '0'
    for year in range(movie_year, 2019):
        try:
            WebDriverWait(browser, 15, 3).until(lambda browser: browser.find_element_by_xpath("//select[@id='selYear']"))
            browser.find_element_by_xpath("//select[@id='selYear']/option[@value='" + str(year) + "']").click()
            time.sleep(1)
            browser.find_element_by_xpath("//input[@id='btnSearch']").click()
            time.sleep(1)
            next_page = browser.find_elements_by_xpath("//ul[@id='ulpage']/li")[-1]
            time.sleep(1)
            total_pages = next_page.get_attribute("onclick").split("1,")[1].replace(")", "")
            print total_pages
            for page in range(int(crawling_page)+1, int(total_pages)+1):
                page_url = 'http://www.cbooo.cn/Mdata/getMdata_movie?area=50&type=0&year=' + str(movie_year) + '&initial=全部&pIndex=' + str(page)
                print "共有" + total_pages + "页。现在爬取第" + str(page) + "页：" + page_url
                html = urllib2.urlopen(page_url)
                time.sleep(1)
                json_content = json.loads(html.read())
                movie_content = json_content["pData"]
                movie_list = []
                for movie in movie_content:
                    movie_year = str(year)
                    movie_name = movie['MovieName']
                    movie_id = movie['ID']
                    movie_url = 'http://www.cbooo.cn/m/'+movie_id
                    print movie_year, movie_name, movie_url, movie_id
                    time.sleep(0.5)
                    with open("../data/movies.txt", "a+")as f:
                        f.write(movie_name + "``" + movie_year + "\n")
                    movie_list.append(movie_year)
                    movie_list.append(movie_name)
                    movie_list.append(movie_url)
                    movie_list.append(movie_id)
                    time.sleep(0.5)
                name = movie_site + str(year)
                time.sleep(1)
                connect_redis.__redis_storage(name, movie_list)
                time.sleep(1)
                with open("../movie_sites/" + movie_site + "/crawled_year.txt", "a+")as m:
                    m.write(str(year) + "`" + total_pages + "`" + str(page) + "\n")
        except:
            browser.close()
            time.sleep(120)
            __cbooo_get(second_movie_website)


def __douban_get(movie_site):
    # 集合法断点重续
    total_movies = set()
    crawled_movies = set()
    error_movies = set()
    with open("../data/movies.txt", "r")as f:
        line = f.readlines()
        for r in range(1, len(line)):
            total_movies.add(line[r].replace("\n", ""))
    print "全部电影集合完成！！"
    with open("../data/movies_crawled.txt", "r")as m:
        lines = m.readlines()
        for line in lines:
            crawled_movies.add(line.replace("\n", ""))
    print "已爬电影集合完成！！"
    with open("../movie_sites/豆瓣网/movie_error.log", "r")as n:
        liness = n.readlines()
        for line in liness:
            error_movies.add(line.replace("\n", ""))
    print "出错电影集合完成！！"
    movies = set(total_movies - (crawled_movies | error_movies))
    for movie in movies:
        movie_name = movie.split("``")[0]
        print type(movie_name)
        movie_year = movie.split("``")[1]
        print movie_name, movie_year
        movie_url = 'https://movie.douban.com/subject_search?search_text=' + urllib.quote(movie_name) + '&cat=1002'
        browser.get(movie_url)
        time.sleep(2)
        try:
            WebDriverWait(browser, 20, 2).until(lambda browser: browser.find_element_by_xpath("//div[@id='root']"))
            search_result = browser.find_elements_by_xpath("//div[@class='title']")
            flag = 0
            movie_list = []
            for result in search_result:
                time.sleep(0.2)
                try:
                    name = result.find_element_by_xpath("a")
                    if movie_year in name.text or str(int(movie_year)+1) in name.text or str(int(movie_year)-1) in name.text:
                        movie_url = name.get_attribute("href")
                        print movie_url,
                        movie_id = movie_url.split("subject/")[1].replace("/", "")
                        print movie_id
                        with open("../data/movies_crawled.txt", "r")as n:
                            n.write(movie_name+"``"+movie_year+"\n")
                        movie_list.append(movie_year)
                        movie_list.append(movie_name)
                        movie_list.append(movie_url)
                        movie_list.append(movie_id)
                        time.sleep(0.5)
                        name = movie_site + str(movie_year)
                        time.sleep(1)
                        connect_redis.__redis_storage(name, movie_list)
                        time.sleep(1)
                        break
                    else:
                        flag = 1 + flag
                        print "this movie is wrong!"
                except:
                    flag = 1 + flag
                    print "can not find name!!!"
                    pass
            if flag == int(len(search_result)):
                with open("../movie_sites/豆瓣网/movie_error.log", "a+")as n:
                    n.write(movie_name+"``"+movie_year+"\n")
        except:
            time.sleep(120)
            __douban_get(third_movie_website)


def __58921_get(movie_site):
    with open("../movie_sites/"+movie_site+"/crawled_year.txt", "r")as f:
        lines = f.readlines()
    if len(lines) > 0:
        crawling_year = lines[-1].split("`")[0]
        total_page = lines[-1].split("`")[1]
        crawling_page = lines[-1].split("`")[2].replace("\n", "")
        print crawling_year, total_page, crawling_page
    else:
        crawling_year = '2007'
        total_page = '-1'
        crawling_page = '0'
        print crawling_year, total_page, crawling_page
    if total_page != crawling_page:
        movie_year = int(crawling_year)
    else:
        movie_year = int(crawling_year)+1
        crawling_page = '0'
    for year in range(movie_year, 2019):
        year_url = 'http://58921.com/alltime/' + str(year)
        browser.get(year_url)
        time.sleep(1)
        try:
            WebDriverWait(browser, 10, 2).until(lambda browser: browser.find_element_by_xpath("//div[@class='item-list item_pager']"))
            total_movies = browser.find_element_by_xpath("//div[@class='item-list item_pager']//span[@class='pager_number']").text
            if int(total_movies) % 20 == 0:
                for page in range(int(crawling_page), int(total_movies)/20):
                    page_url = year_url + '?page=' + str(page)
                    print "共有", int(total_movies) / 20, "页,", "第", page+1, "页：", page_url
                    browser.get(page_url)
                    time.sleep(1)
                    movie_list = []
                    try:
                        WebDriverWait(browser, 15, 3).until(lambda browser: browser.find_element_by_xpath("//div[@class='table-responsive']"))
                        movies = browser.find_elements_by_xpath("//div[@class='table-responsive']//tbody/tr")
                        for movie in movies:
                            time.sleep(0.2)
                            print year,
                            movie_name = movie.find_elements_by_xpath("td")[2].text
                            print movie_name,
                            movie_url = movie.find_element_by_xpath("td/a").get_attribute("href")
                            print movie_url,
                            movie_id = movie_url.split('/film/')[1]
                            print movie_id
                            time.sleep(0.1)
                            movie_list.append(year)
                            movie_list.append(movie_name)
                            movie_list.append(movie_url)
                            movie_list.append(movie_id)
                        name = movie_site + str(year)
                        time.sleep(1)
                        movie_list = []
                        connect_redis.__redis_storage(name, movie_list)
                        time.sleep(1)
                        with open("../movie_sites/" + movie_site + "/crawled_year.txt", "a+")as m:
                            m.write(str(year) + "`" + str(int(total_movies)/20) + "`" + str(page+1) + "\n")
                    except:
                        browser.close()
                        time.sleep(120)
                        __58921_get(first_movie_website)
            if int(total_movies) % 20 != 0:
                for page in range(0, int(total_movies)/20+1):
                    page_url = year_url + '?page=' + str(page)
                    print "共有", int(total_movies) / 20+1, "页,", "第", page+1, "页：", page_url
                    browser.get(page_url)
                    time.sleep(1)
                    try:
                        WebDriverWait(browser, 15, 3).until(lambda browser: browser.find_element_by_xpath("//div[@class='table-responsive']"))
                        movies = browser.find_elements_by_xpath("//div[@class='table-responsive']//tbody/tr")
                        for movie in movies:
                            time.sleep(0.2)
                            print year,
                            movie_name = movie.find_elements_by_xpath("td")[2].text
                            print movie_name,
                            movie_url = movie.find_element_by_xpath("td/a").get_attribute("href")
                            print movie_url,
                            movie_id = movie_url.split('/film/')[1]
                            print movie_id
                            time.sleep(0.1)
                            movie_list.append(year)
                            movie_list.append(movie_name)
                            movie_list.append(movie_url)
                            movie_list.append(movie_id)
                        name = movie_site + str(year)
                        time.sleep(1)
                        connect_redis.__redis_storage(name, movie_list)
                        time.sleep(1)
                        with open("../movie_sites/" + movie_site + "/crawled_year.txt", "a+")as m:
                            m.write(str(year) + "`" + str(int(total_movies)/20+1) + "`" + str(page+1) + "\n")
                    except:
                        browser.close()
                        time.sleep(120)
                        __58921_get(first_movie_website)
        except:
            browser.close()
            time.sleep(120)
            __58921_get(first_movie_website)


def main(first, second, third):
    login.__58921_login(browser)
    time.sleep(2)
    __58921_get(first)
    print "电影排片数据库爬取成功！"
    time.sleep(2)
    __cbooo_get(second)
    print "中国票房网爬取成功！"
    time.sleep(2)
    login.__douban_login(browser)
    __douban_get(third)
    print "豆瓣网爬取成功！"
    connect_redis.__main()
    print "数据存储成功！"


def start():
    try:
        main(first_movie_website, second_movie_website, third_movie_website)
        restart_58921.error_flags = True
    except Exception, a:
        print Exception, ":", a
        try:
            while True:
                browser.close()
        except Exception, e:
            print Exception, ":", e
    finally:
        browser.quit()
        sys.exit()


if __name__ == '__main__':
    first_movie_website = '电影排片数据库'
    second_movie_website = '中国票房网'
    third_movie_website = '豆瓣网'
    if not os.path.exists("../movie_sites/"+first_movie_website):
        os.mkdir("../movie_sites/"+first_movie_website)
    if not os.path.exists("../movie_sites/"+second_movie_website):
        os.mkdir("../movie_sites/"+second_movie_website)
    if not os.path.exists("../movie_sites/"+third_movie_website):
        os.mkdir("../movie_sites/"+third_movie_website)
    start()