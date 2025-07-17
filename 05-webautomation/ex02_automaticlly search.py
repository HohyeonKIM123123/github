from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com")

search_box = driver.find_element(By.NAME, "q")  #serching for name="q"  cus that is the search tab
search_box.send_keys("Selenium Python")  #google detect and think it as a computer cus it's sooo fast 
search_box.send_keys(Keys.RETURN)  #(return is enter)
time.sleep(50)