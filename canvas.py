from PIL import Image
import pandas as pd
import urllib.request
from io import BytesIO
import requests
import random

csv = pd.read_csv(r"C:\Users\ashar\Documents\GitHub\Trial Python Pillow\Agama_DB.csv")

csv = csv.dropna(axis=0,).reset_index(drop=True)
csv = csv.drop('Unnamed: 0', axis= 1)
csv.to_csv("new.csv")

# background = image.open("background500.jpg")

# for x in linkfoto:
#     print(x)
#     response = requests.get(x)
#     buku = image.open(bytesio(response.content))
#     # height = int(buku.height) / int(buku.height)
#     # new_height = int(627 * height)
#     buku = buku.resize([260 ,422])
#     background.paste(buku,(202,40))
#     name = x[int(x.find("produk/")+7):int(x.find(".jpg")+4)]
#     background.save(f'{name}.jpg')