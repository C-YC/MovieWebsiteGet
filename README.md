# MovieWebsiteGet
Get the year, name, link, and ID of the movie from five movie sites, and store the data in the redis database, and finally retrieve the data from redis and store it as a csv file.<br>
<img src="https://github.com/C-YC/MovieWebsiteGet/blob/master/data/360347164.jpg" width="600" height="300"/>
# Main codes
`get_contents.py`<br>
main code to get info from the websites 
[中国票房网](http://www.cbooo.cn/movies),
[豆瓣电影](https://movie.douban.com/),
[中国排片数据库](http://58921.com/alltime)<br>
`mtime_1905_get.py`<br>
main code to get info from the websites 
[时光网](http://movie.mtime.com/movie/search/section/#),
[1905电影网](http://www.1905.com/mdb/film/search/)<br>
`login.py`<br>
89521 website user account login<br>
`connect_redis.py`<br>
store data in and out of the redis<br>
`restart.py`<br>
determine whether there is an error and whether to restart get_contents.py, mtime_1905_get.py<br>
`start.sh`
script to start the program <br>
# Operating environment
Based on **python2.7** and **selenium**, first need to install：<br>
* selenium
* geckodriver
* pandas
* redis
([tutorial](http://www.runoob.com/redis/redis-tutorial.html)):<br>
> Install redis under Ubuntu <br>
```
$ sudo apt-get update
$ sudo apt-get install redis-server
```
> Start Redis <br>
```
$ redis-server
```
> See if redis has started (redis 127.0.0.1:6379> 127.0.0.1 是本机 IP ，6379 是 redis 服务端口)
```
$ redis-cli
redis 127.0.0.1:6379> ping
PONG
```
# Operation instructions
|start.sh|—>|restart.py|—>|get_contents.py/mtime_1905_get.py|
|:---|:---|:---|:---|:---|

Open the terminal in the directory where the files are stored.<br>
Input:<br>
**sh start.sh**
# Bullet points
Key skills that I have learned <br>
1.Breakpoint renewed <br>
<img src="https://github.com/C-YC/MovieWebsiteGet/blob/master/data/%E6%96%AD%E7%82%B9%E9%87%8D%E7%BB%AD.png" width="600" height="350"/> <br>
2.redis <br>
[Specific operation：Python operates on redis](https://www.cnblogs.com/melonjiang/p/5342505.html)
```
import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
r.sadd(key_name)                    # set()操作，存储
content = r.smembers(key_name)      # 获取数据
```
<img src="https://github.com/C-YC/MovieWebsiteGet/blob/master/data/redis_set.png" width="600" height="250"/> <br>
(Other data type operation for redis in the **data** directory)
# Sample
Data storage format <br>
Data is stored according to different websites and different years. <br>
For example, the movie of the 58921 movie website in 2007 is stored as shown below. <br>
<img src="https://github.com/C-YC/MovieWebsiteGet/blob/master/data/58921%E7%BD%91%E7%AB%99.png" width="500" height="120"/> <br>
* csv files lables <br>

|movie_id|movie_name|movie_url|movie_year|
|:---|:---|:---|:---|
