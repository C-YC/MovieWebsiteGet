# -*- coding:utf-8 -*-
"""
author:C-YC
target:爬取时光网和1905电影网07～18年电影的名字、链接、id，并存入redis中
finish date：2018,07,29
"""
import sys
import time
import os
import restart
import connect_redis
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
reload(sys)
sys.setdefaultencoding("utf-8")
browser = webdriver.PhantomJS(executable_path='./phantomjs')


def __mtime_get(movie_site):
    # 断点重续：将爬取成功的年份与页数记录下来，当下次调用函数时可以直接从下一页开始
    with open("../movie_sites/"+movie_site+"/crawled_year.txt", "r")as f:
        lines = f.readlines()
    if len(lines) > 0:
        crawling_year = lines[-1].split("`")[0]
        total_page = lines[-1].split("`")[1]
        crawling_page = lines[-1].split("`")[2].replace("\n", "")
        print crawling_year, total_page, crawling_page
    else:
        # 第一次调用函数时，将总页数记为-1,从0页开始
        crawling_year = '2007'
        total_page = '-1'
        crawling_page = '0'
        print crawling_year, total_page, crawling_page
    # 当总页数与已获取页数不一样时，年份不变
    if total_page != crawling_page:
        movie_year = int(crawling_year)
    else:
        # 一样时，年份增加一年，已获取页数为0
        movie_year = int(crawling_year)+1
        crawling_page = '0'
    for year in range(movie_year, 2019):
        year_url = 'http://movie.mtime.com/movie/search/section/#year=' + str(year)
        browser.get(year_url)
        time.sleep(2)
        try:
            WebDriverWait(browser, 20, 5).until(lambda browser: browser.find_element_by_xpath("//div[@class='mt15 mr15']"))
            movie_num = browser.find_element_by_xpath("//div[@class='mt15 mr15']//h4[@class='px14']").text.split('共')[1].replace('部', '')
            if int(movie_num) % 20 == 0:
                for page in range(int(crawling_page)+1, int(movie_num)/20 + 1):
                    page_url = year_url + '&pageIndex=' + str(page)
                    print "共有", int(movie_num)/20, "页,", "第", page, "页：", page_url
                    browser.get(page_url)
                    time.sleep(1)
                    browser.refresh()
                    time.sleep(2)
                    try:
                        WebDriverWait(browser, 15, 5).until(lambda browser: browser.find_element_by_xpath("//ul[@class='ser_mlist2']"))
                        movies = browser.find_elements_by_xpath("//ul[@class='ser_mlist2']//h3[@class='normal mt6']")
                        print len(movies)
                        movie_list = []
                        for movie in movies:
                            time.sleep(0.2)
                            print year,
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
                        # 每获取20部电影，按年份，名字，链接，id存成列表，一起存入redis中
                        name = movie_site+str(year)
                        time.sleep(1)
                        connect_redis.__redis_storage(name, movie_list)
                        time.sleep(1)
                        # 爬取成功，记录文件
                        with open("../movie_sites/"+movie_site+"/crawled_year.txt", "a+")as m:
                            m.write(str(year) + "`" + str(int(movie_num)/20) + "`" + str(page) + "\n")
                    except:
                        time.sleep(120)
                        __mtime_get(first_movie_website)
            if int(movie_num) % 20 != 0:
                for page in range(int(crawling_page)+1, int(movie_num)/20 + 2):
                    page_url = year_url + '&pageIndex=' + str(page)
                    print "共有", int(movie_num) / 20 + 1, "页,", "第", page, "页：", page_url
                    browser.get(page_url)
                    time.sleep(1)
                    browser.refresh()
                    time.sleep(2)
                    try:
                        WebDriverWait(browser, 15, 5).until(lambda browser: browser.find_element_by_xpath("//ul[@class='ser_mlist2']"))
                        movies = browser.find_elements_by_xpath("//ul[@class='ser_mlist2']//h3[@class='normal mt6']")
                        print len(movies)
                        movie_list = []
                        for movie in movies:
                            time.sleep(0.2)
                            print year,
                            movie_name = movie.find_element_by_xpath("a").text
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
                        name = movie_site + str(year)
                        time.sleep(1)
                        connect_redis.__redis_storage(name, movie_list)
                        time.sleep(1)
                        with open("../movie_sites/" + movie_site + "/crawled_year.txt", "a+")as m:
                            m.write(str(year) + "`" + str(int(movie_num)/20+1) + "`" + str(page) + "\n")
                    except:
                        time.sleep(120)
                        __mtime_get(first_movie_website)
        except:
            browser.quit()
            sys.exit()


def __1905_get(movie_site):
    with open("../movie_sites/"+movie_site+"/crawled_year.txt", "r")as f:
        lines = f.readlines()
    if len(lines) > 0:
        crawling_year = lines[-1].split("`")[0]
        total_page = lines[-1].split("`")[1]
        crawling_page = lines[-1].split("`")[2].replace("\n", "")
        print crawling_year, crawling_page
    else:
        crawling_year = '2007'
        total_page = '-1'
        crawling_page = '0'
        print crawling_year, crawling_page
    if total_page != crawling_page:
        movie_year = int(crawling_year)
    else:
        movie_year = int(crawling_year)+1
        crawling_page = '0'
    for year in range(movie_year, 2019):
        year_url = 'http://www.1905.com/mdb/film/list/year-' + str(year) + '/'
        browser.get(year_url)
        time.sleep(1)
        try:
            WebDriverWait(browser, 10, 2).until(lambda browser: browser.find_element_by_xpath("//div[@class='lineG pl10 pb12']"))
            movie_num = browser.find_element_by_xpath("//div[@class='lineG pl10 pb12']").text.replace("共", "").replace("部影片", "")
            print movie_num
            if int(movie_num) % 30 != 0:
                for page in range(int(crawling_page)+1, int(movie_num) / 30 + 2):
                    page_url = year_url + 'o0d0p' + str(page) + '.html'
                    print "共有", int(movie_num) / 30 + 1, "页,", "第", page, "页：", page_url
                    browser.get(page_url)
                    time.sleep(2)
                    try:
                        WebDriverWait(browser, 15, 3).until(lambda browser: browser.find_element_by_xpath("//div[@class='leftArea']"))
                        movies = browser.find_elements_by_xpath("//div[@class='leftArea']/ul[@class='inqList pt18']/li")
                        movie_list = []
                        for movie in movies:
                            print year,
                            time.sleep(0.1)
                            movie_name = movie.find_element_by_xpath("div[@class='text']/p/a").text
                            print movie_name,
                            movie_url = movie.find_element_by_xpath("div[@class='text']/p/a").get_attribute("href")
                            print movie_url,
                            movie_id = movie_url.split('/film/')[1].replace("/", "")
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
                            m.write(str(year) + "`" + str(int(movie_num)/30+1) + "`" + str(page) + "\n")
                    except:
                        browser.close()
                        time.sleep(120)
                        __1905_get(second_movie_website)
            if int(movie_num) % 30 == 0:
                for page in range(int(crawling_page)+1, int(movie_num) / 30 + 1):
                    page_url = year_url + 'o0d0p' + str(page) + '.html'
                    print "共有", int(movie_num) / 30, "页,", "第", page, "页：", page_url
                    browser.get(page_url)
                    time.sleep(2)
                    try:
                        WebDriverWait(browser, 15, 3).until(lambda browser: browser.find_element_by_xpath("//div[@class='leftArea']"))
                        movies = browser.find_elements_by_xpath("//div[@class='leftArea']/ul[@class='inqList pt18']/li")
                        movie_list = []
                        for movie in movies:
                            print year,
                            time.sleep(0.1)
                            movie_name = movie.find_element_by_xpath("div[@class='text']/p/a").text
                            print movie_name,
                            movie_url = movie.find_element_by_xpath("div[@class='text']/p/a").get_attribute("href")
                            print movie_url,
                            movie_id = movie_url.split('/film/')[1].replace("/", "")
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
                            m.write(str(year) + "`" + str(int(movie_num)/30) + "`" + str(page) + "\n")
                    except:
                        browser.close()
                        time.sleep(120)
                        __1905_get(second_movie_website)
        except:
            browser.close()
            time.sleep(120)
            __1905_get(second_movie_website)


def main():
    __mtime_get(first_movie_website)
    time.sleep(2)
    __1905_get(second_movie_website)


def start():
    try:
        main()
        restart.error_flags = True
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
    first_movie_website = 'Mtime时光网'
    second_movie_website = '1905电影网'
    if not os.path.exists("../movie_sites/"+first_movie_website):
        os.mkdir("../movie_sites/"+first_movie_website)
    if not os.path.exists("../movie_sites/"+second_movie_website):
        os.mkdir("../movie_sites/"+second_movie_website)
    start()