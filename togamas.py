# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import socket
import time
import random

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Product link (empty)
productlinks = []

# Configuring selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
service = Service(r'C:\Users\ashar\Documents\GitHub\Project-Scraping-Mizan\chromedriver.exe')
driver = webdriver.Chrome(service = service, options= chrome_options)

driver.set_window_size(1280,720)
driver.get("https://togamas.com/koleksi-3")
time.sleep((50))
driver.save_screenshot('0.png')
for i in range(1,16):
    scroll = 1500 * i
    driver.execute_script(f"window.scrollTo(0, {scroll})")
    time.sleep((5))
    driver.save_screenshot(f'{i}.png')
    print(f"loading : {i}")
    
baseurl = "https://togamas.com/"
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
lists = soup.find_all('li', class_= "boxProduk back_rand")
for x in lists:
    for a in x('a', href=True):
        link = baseurl + a.get('href')
        productlinks.append(link)

print(productlinks)
# content.find_elements