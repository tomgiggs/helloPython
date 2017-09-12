from selenium import webdriver
import  time
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')
elem = browser.find_element_by_id("kw")
elem.send_keys("selenium")
browser.find_element_by_id("su").click()

time.sleep(1)
print browser.page_source
browser.close()
