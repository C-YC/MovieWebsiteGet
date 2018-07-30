# -*- coding:utf-8 -*-
"""
author:C-YC
target:连接redis，存储数据，提取数据
finish date：2018,07,29
"""
import redis
import time
import pandas as pd


def __redis_storage(name_key, movie_list):
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)
    r.sadd(name_key, movie_list)
    time.sleep(1)
    # print r.smembers(name_key)


def __redis_get(site, year, name_key):
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)
    time.sleep(1)
    contents = str(r.smembers(name_key)).decode("unicode_escape")
    print contents
    content = contents.replace("set([\"[", "").replace("]\", '[]', \"[", ", ").replace("]\", \"[", ", ")\
        .replace("]\', \'[", ", ").replace("]\", \'[", ", ").replace("]\"])", "").replace("u\'", "").replace("\'", "")\
        .replace("\"", "").replace("[", "").replace("]", "").split(", ")
    print len(content)
    print type(content)
    movie_list = []
    for r in range(0, len(content), 4):
        row = {}
        row['movie_year'] = content[r].encode('utf-8')
        row['movie_name'] = content[r+1].decode('unicode_escape').encode('utf-8')   # 处理其他网站中文数据
        # row['movie_name'] = content[r+1].decode('string_escape').encode('utf-8')  # 处理豆瓣网中文数据
        row['movie_url'] = content[r+2].encode('utf-8')
        row['movie_id'] = content[r+3].encode('utf-8')
        time.sleep(0.1)
        print row
        movie_list.append(row)
    movie_info = pd.DataFrame(movie_list)
    time.sleep(2)
    movie_info.to_csv("../movie_sites/"+site+"/movie_"+str(year)+".csv", index=False, sep=',')


def __main():
    websites = ['1905电影网', 'Mtime时光网', '中国票房网', '电影排片数据库', '豆瓣网']
    for site in websites:
        for year in range(2007, 2009):
            name = site + str(year)
            __redis_get(site, year, name)
            time.sleep(1)
            print name, "successful data storage！！！"

