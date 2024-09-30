from selenium import webdriver
from selenium.webdriver.common.by import By
import time #dung de ngung dong thoi gian

#khoi tao webdriver
driver = webdriver.Chrome()

#mo trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name"
driver.get(url)

#doi 2s
time.sleep(2)

#lay all the <a> voi title chua "list of painters"
tags=driver.find_elements(By.XPATH, "//a[contains(@title, 'List of painters')]") # "//" tuong doi, tim het cac the a

#tao ra ds cac lien ket
links = [tag.get_attribute("href") for tag in tags]

#xuat thong tin
for link in links:
    print(link)

#dong webdriver
driver.quit()