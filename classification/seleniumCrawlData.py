# 引入 requests 模組
import requests
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
# 引入 selenium.webdriver 模組
from selenium import webdriver
# 引入 sleep 模組
from time import sleep

from bs4.element import Comment
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


driver = webdriver.Chrome('./chromedriver')
driver.get("https://www.whsh.tc.edu.tw/ischool/publish_page/0/")  # 前往這個網址

for i in range(50):
    # 以 Beautiful Soup 解析 HTML 程式碼
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for item in soup.find_all("tr", class_="tcontent"):
        if int(item.find("td", field="clicks").get_text()) > 100:  # 點閱超過100
            title = item.find("td", field="title").get_text()
            print(title)
            url = "trainData/"+"".join(c for c in title if c.isalnum())

            driver.find_element_by_xpath('//a[@title=\"'+title+'\"]').click()
            sleep(2)
            if item.select_one('a')["href"] == "javascript:void(0);": #非新頁面
                driver.switch_to.frame(driver.find_element_by_class_name("b-iframe"))  #定位frame
                soupFrame = BeautifulSoup(driver.page_source, 'html.parser').find("div", id="div_news_table_1_content")
                driver.switch_to.default_content()
                driver.find_element_by_class_name('bClose').click()
            else:
                soupFrame = BeautifulSoup(driver.page_source, 'html.parser')
                actions = ActionChains(driver) 
                actions.send_keys(Keys.CONTROL + 'w')
                actions.perform()
            f = open(url + ".txt", "w")
            f.write(" ".join(t.strip()
                            for t in filter(tag_visible, soupFrame.findAll(text=True))))
            f.close()
                

    driver.find_element_by_id("btnNext").click()
    sleep(3)

driver.close()
