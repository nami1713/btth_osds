from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#khoi tao WebDriver
driver = webdriver.Chrome()

#mo mot trang web
driver.get("https://gomotungkinh.com")

time.sleep(5000)

#tim phan tu img co id la "bonk"
bonk_img= driver.find_element(By.ID, value="bonk")

#click lien tuc vao img bonk
while True:
    bonk_img.click()
    print("Clicked on the bonk image")
    time.sleep(0.1)