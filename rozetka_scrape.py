import requests
from bs4 import BeautifulSoup
import pprint
from PIL import Image
import urllib.request
import pandas as pd

# Working with rozetka's url
URL = "https://hard.rozetka.com.ua/computers/c80095/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


# looking for products area
results = soup.find(class_='layout layout_with_sidebar')

# creating a list of every single product (still HTML)
products = results.find_all('li', class_='catalog-grid__cell catalog-grid__cell_type_slim')

# creating a dic for future df
dfProducts = {"Title":[], 'Price':[], 'Specs': [], 'Link':[]}

# empty list of imgs of products
img_urls = []

# empty list of every product page
product_urls = []

# filling the dic with data from HTML 
for product in products:
        product_title = product.find('span', class_='goods-tile__title')
        product_Price = product.find('div', class_='goods-tile__price goods-tile__price_color_red')
        product_link = product.find('a')['href']
        if None in (product_link, product_Price, product_title):
            continue
        dfProducts['Title'].append(product_title.text)
        dfProducts['Price'].append(product_Price.text)
        dfProducts['Link'].append(product_link)
        product_urls.append(product_link)
        # filling the img_urls list with urls from HTML
        for img in product.find_all('img'):
            try:
                img_url = img['data-url']
            except:
                continue
            img_urls.append(img_url)



# creating a new request of every product's page
for product_url in product_urls:

        pageResult = requests.get(product_url+'characteristics/')
        soup = BeautifulSoup(pageResult.content, 'html.parser')
        results = soup.find(class_='product-characteristics__group')
        try:    
            info = results.find_all('ul', class_='product-characteristics__sub-list')
            dfProducts['Specs'].append(info[0].text)
            # print(info[0].text)
        except:
            continue

# creating df
df = pd.DataFrame(data = dfProducts)
# print(df)

# saving the df in .csv format
df.to_csv('products.csv', encoding='utf-8-sig')

# setting the path for downloading imgs
IMAGE_PATH = "./computers/"

# function to download images
def download_images(i, img_url, file_path):
    filename = 'image-{}.jpg'.format(i)
    full_path = '{}{}'.format(file_path,filename)
    urllib.request.urlretrieve(img_url, full_path)

    print( '{} saved'.format(filename) )

    return None


# call the function to download images

# for i, url in enumerate(img_urls):
#     download_images(i, url, IMAGE_PATH)
