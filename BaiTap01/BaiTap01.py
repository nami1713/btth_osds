from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

######################################################
# I. Tai noi chua links va Tao dataframe rong
all_links = []
musician_links=[]
d = pd.DataFrame({'name of the band': [], 'years active': []})
######################################################
# II. Lay ra tat ca duong dan de truy cap den musicians
# Khởi tạo Webdriver
for i in range(65,66):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/Lists_of_musicians"
    try:

        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(0.5)

        # Lay ra tat ca cac the ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # try ul thu 20
        ul_musicians = ul_tags[21]  # list start with index=0

        # Lay ra tat ca the <li> thuoc ul_musicians
        li_tags = ul_musicians.find_elements(By.TAG_NAME, "li")

        # Tao danh sach cac url
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)
        # tao danh sach cac title
        titles = [tag.find_element(By.XPATH, "//div[contains(@class,'div-col')]").get_attribute("title") for tag in li_tags]
    except:
        print("Error!")

    # Dong webdriver
    driver.quit()
######################################################
# III. Lay thong tin cua tung musician
count =0;
for link in all_links:
    print(link)
    # Khoi tao webdriver
musician_driver = webdriver.Chrome()
musician_driver.get(all_links[0])
time.sleep(0.5)

try:
     #lấy tất cả các the ul của list of acid rock artists
    ul_artists_tags = musician_driver.find_elements(By.TAG_NAME, "ul")
    print(len(ul_artists_tags))

    #chọn ul thứ 25
    ul_artist = ul_artists_tags[24]
    #lấy tất cả link chứa thông tin thuộc artists
    li_artist = ul_artist.find_elements(By.TAG_NAME, "li")
    print(len(li_artist))

    # tạo danh sách các url của artist
    links_artist = [artist_tag.find_element(By.TAG_NAME,"a").get_attribute("href") for artist_tag in li_artist]
    for x in links_artist:
        musician_links.append(x)
except:
    print("Error!")
#dong webdriver
musician_driver.quit()

#lay thong tin cua tung nhac si
count = 0
for link in musician_links:
    if (count >= 20):
        break
    count += 1
    print(link)
    try:
        # khoi tao webdriver
        driver = webdriver.Chrome()
        # mo trang
        url = link
        driver.get(url)
        # doi 2s
        time.sleep(2)
        # lay ten nhac si/ban nhac
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # lay năm hoat dong
        try:
            year_element = driver.find_element(By.XPATH, value='//span[contains(text(),"Years active")]/parent::*/following-sibling::td')
            year = year_element.text

        except:
            year = ""

        # tao dictionary thong tin hoa si
        musicians = {'name of the band': name, 'years active': year}
        # chuyen doi dictionary thanh dataframe
        musicians_df = pd.DataFrame([musicians])
        # them thong tin vao df chinh
        d = pd.concat([d, musicians_df], ignore_index=True)
        # dong web
        driver.quit()
    except:
        print("Error!!!")

# IV.In thong tin ra file excel
d
#dat ten file excel
file_name = "Musicians.xlsx"
# saving the excel
d.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')