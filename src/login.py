# -*- coding:utf-8 -*-
"""
author:C-YC
target:用于不同电影网站的用户登录
finish date：2018,07,2
"""
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")


def __58921_login(browser):
    browser.get("http://58921.com/user/login")
    time.sleep(2)
    user_mailbox = '1425575659@qq.com'
    user_pw = 'zxcvbnm,'
    browser.find_element_by_xpath("//div[@class='user_login_form']//input[@id='user_login']").send_keys(user_mailbox)
    time.sleep(1)
    browser.find_element_by_xpath("//div[@class='user_login_form']//input[@id='user_login_form_type_pass']").send_keys(user_pw)
    time.sleep(2)
    browser.find_element_by_xpath("//div[@id='user_login_form_submit']/input").click()


def __douban_login(browser):
    browser.get("https://www.douban.com/accounts/login?source=movie")
    time.sleep(2)
    user_mailbox = '1425575659@qq.com'
    user_pw = 'zxcvbnm,233'
    user_number = browser.find_element_by_xpath("//input[@id='email']")
    time.sleep(1)
    user_number.clear()
    time.sleep(1)
    user_number.send_keys(user_mailbox)
    time.sleep(1)
    browser.find_element_by_xpath("//input[@id='password']").send_keys(user_pw)
    time.sleep(2)
    browser.find_element_by_xpath("//input[@class='btn-submit']").click()
