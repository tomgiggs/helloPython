import traceback
import traceback
import requests
import urllib
import urllib2
import cookielib


import requests
import selenium
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By


def seleniumtest():
    driver = webdriver.Chrome()
    page =driver.get('https://www.cnblogs.com/qingchunjun/p/4208159.html')
    #form = driver.find_element_by_name('h2')
    h2 = driver.find_element_by_tag_name('h2')
    form = driver.find_element_by_class_name('posthead')
    try:
        click = driver.find_element_by_xpath('//div[@id="leftmenu"]//div[@id="profile_block"]//a')
        print click.text
        action = ActionChains(driver)

        action.click(click)

    except:
        print traceback.print_exc()
        pass
    if form:
        print 'you need login'
        print form.text
    try:
        action = ActionChains(driver)
        action.click(h2)
        # action.click(click)
    except:
        print traceback.print_exc()

    finally:
        pass
        #driver.close()


def test():
    url = 'https://gitee.com/'
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    urllib2.install_opener(opener)
    headers = {}

    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0'
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    for item in jar:
        print item
    #print dict(jar)
    print response.headers
    print response.headers['Set-Cookie']

test()