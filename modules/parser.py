import os.path
import time

import bs4.element
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.363245"
}

def get_categories(file_name):
    text = open(f'times_file/{file_name}', 'r', encoding='UTF-8').read()
    categories_data = []
    soup = BeautifulSoup(text, 'html.parser')
    cats = soup.find(class_='cats')
    categories = cats.find_all(class_='item')
    for category in categories:

        href = category.attrs.get('href')
        name = category.find(class_='title').text

        categories_data.append({
            'slug': href.split('/')[-1],
            'name': name,
        })
    return categories_data

def return_only_numbers(text):
    value = ''.join([i for i in text if i.isdigit() or i == ',']).replace(',','.')
    return float(value)


def get_products_by_category(category='sushi', category_id=1):

    path = os.path.join(f'times_file', f'{category}.html')

    with open(path, 'r', encoding='UTF-8') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')
    products = soup.find_all(class_='product')

    if not products:
        print()

    data_products = []
    driver = webdriver.Chrome()
    driver.maximize_window()

    for product in products:
        product: bs4.element.Tag = product
        href = product.find(name='a').attrs.get('href')

        driver.get(href)
        time.sleep(1)
        try:
            description = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[2]').text
        except:
            description = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]').text

        paths_ul = [
            '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[4]/div[1]',
            '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[1]',
            '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[1]/ul/li[1]',
        ]
        for path_ul in paths_ul:
            try:
                check = driver.find_element(By.XPATH, f'{path_ul}/ul/li[1]').text
                break
            except:
                continue




        try:
            data_products.append(dict(
                name=driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/h1').text,
                slug=href.split('/')[-1],
                price=return_only_numbers(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]').text),
                description=description,
                category_id=category_id,
                available=True,
                photo=driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]').get_attribute('data-src'),
                weight=return_only_numbers(driver.find_element(By.XPATH, f'{path_ul}/ul/li[1]').text),
                calories=return_only_numbers(driver.find_element(By.XPATH, f'{path_ul}/ul/li[2]').text),
                protein=return_only_numbers(driver.find_element(By.XPATH, f'{path_ul}/ul/li[3]').text),
                fat=return_only_numbers(driver.find_element(By.XPATH, f'{path_ul}/ul/li[4]').text),
                carbohydrates=return_only_numbers(driver.find_element(By.XPATH, f'{path_ul}/ul/li[5]').text),
            ))
        except:
            print()

    return data_products