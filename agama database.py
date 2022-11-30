# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import socket
import time

# Configuring socket for scraping
socket.getaddrinfo('localhost', 8080)

# Product link (empty)
productlinks = set()

# Fetch loop to get product link on every page
for i in range(0,1400,20):
    # page url
    baseurl = f"https://mizanstore.com/kategoriproduk/556_agama_dan_spiritualitas/{i}"
    
    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = service, options= chrome_options)
    
    # Getting the page source from url
    driver.get(baseurl)
    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    # Looking for link on every product
    lists = soup.find_all('div', class_= "ms-product-item pull-left")
    for item in lists:
        for link in item.find_all("a", alt="produk", href=True):
            productlinks.add(link['href'])
    print(f"Total Product Link Added : ", len(productlinks))
    
# Product links
productlinks = list(productlinks)

# Product list
product = []

# Scraping information on every product links 
for x in productlinks:
    # Assigning product link
    url = x
    
    # Configuring selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service = service, options= chrome_options)
    
    # Getting the page source from url
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    # scrape the product title 
    try:
        judul = soup.find(id="tag_judul").text
    except:
        judul = "undefined"
    
    # scrape product description
    try:
        deskripsi = soup.find(id="desk").text.strip()
    except:
        deskripsi = "undefined"
        
    # scrape product stock
    try : 
        if soup.find("a", class_="btn-1 sm shadow-0" ).text ==  "produk tidak tersedia":
            stok = "0"
        else:
            stok = soup.find("a", class_="btn-1 sm shadow-0" ).text
    except:
        stok = "undefined"
    
    # scrape product retail price 
    try:
        harga_retail = soup.find('strong' , class_="harga-discount").text
    except:
        harga_retail = "undefined"
        
    # scrape product retail price after discount
    try:
        harga = soup.find('strong' , style="color:#ff8401;").text
    except:
        harga = "undefined"
    
    # scrape product specification
    try: 
        spesifikasi = soup.find("table", class_="table table-striped").text
    except: 
        spesifikasi = "undefined"
    
    # Getting ISBN detail from product specification
    if spesifikasi != "undefined":
        try:
            ISBN = spesifikasi[spesifikasi.find("ISBN")+4:spesifikasi.find("Berat")].strip()
        except : 
            ISBN = "undefined"
    else:
        ISBN = "undefined"
    
    # Getting product weight from product specification
    if spesifikasi != "undefined":
        try:
            berat = spesifikasi[spesifikasi.find("Berat")+5:spesifikasi.find("Dimensi")].strip()
        except:
            berat = "undefined"
    else:
        berat = "undefined"
    
    # Getting product dimension from product specification
    if spesifikasi != "undefined":
        try:
            dimensi = spesifikasi[spesifikasi.find("(P/L/T)")+7:spesifikasi.find("Halaman")].strip()
        except:
            dimensi = "undefined"
    else:
        dimensi = "undefined"
    
    # Getting product page detail from product specification
    if spesifikasi != "undefined":
        try:
            halaman = spesifikasi[spesifikasi.find("Halaman")+7:spesifikasi.find("Jenis")].strip()
        except:
            halaman = "undefined"
    else:
        halaman = "undefined"
    
    
    # Getting product cover detail from product specification
    if spesifikasi != "undefined":
        try :
            cover = spesifikasi[spesifikasi.find("Jenis Cover")+11:spesifikasi.find("Jenis Cover")+22].strip()
        except:
            cover = "undefined"
    else:
        cover = "undefined"
    
    # Getting product photo's link
    try:
        link_foto = soup.find("script", type="application/ld+json").text
        foto = link_foto[link_foto.find('https'):link_foto.find('.jpg')+4]
    except:
        foto = "undefined"
    
    # Getting product's author
    try:
        penerbit = soup.find('strong', style="color:#ff8401; margin-left:5px;").text
    except:
        penerit = "undefined"
    
    # Getting product's publisher
    try:
        pengarang= soup.find('strong', style="color:#ff8401; margin-right:5px;").text
    except:
        penerbit = "undefined"

    # Add all of the product information to dictionary
    data = {
        "judul" : judul,
        "deskripsi" : deskripsi,
        "stok" : stok,
        "harga retail" : harga_retail,
        "harga" : harga,
        "ISBN" :  ISBN,
        "berat" : berat,
        "dimensi" : dimensi,
        "halaman" : halaman,
        "cover" : cover,
        "penerbit" : penerbit,
        "pengarang" : pengarang,
        "link foto" : foto 
        
    }
    
    # add the product dictionary into product list
    product.append(data)
    
    # Downloading the image 
    pic = requests.get(foto, stream = True)
    
    try:
        open(f"{judul}.jpg", 'wb').write(pic.content)
    except:
        judul = re.sub('\W+','', judul)
        open(f"{judul}.jpg", 'wb').write(pic.content)
    
    # Progress Information
    print(f"progress : {len(product)}")
    
# Converting product list into data Frame
df = pd.DataFrame(product)

# Export dataframe into 
df.to_csv("Agama_DB.csv")