from bs4 import BeautifulSoup
import requests
import datetime
import json
import time
import os
import asyncio
import aiohttp
from fake_useragent import UserAgent

# pagination = 140
ua = UserAgent()


def get_data():
    # Download HTML
    # s = requests.Session()
    # for i in range(0, 152, 12):
    #     url = f'https://salomon.kz/man/obuv-2?start={i}'
    #     response = s.get(url=url, headers=headers)
    #     # Создать директорию
    #     if not os.path.exists('html'):
    #         os.mkdir('html')
    #     with open(f'html/data_{i}.html', 'w') as file:
    #         file.write(response.text)
    #     print(f'[+] html_{i} done')
    # exit()

    # Download JSON
    count = 0
    pages = 0
    result = []
    limit = 60
    offset = 0
    min_price = 2000  # USD
    max_price = 10000  # USD

    while True:
        for item in range(offset, offset + limit, limit):
            url = f'https://cs.money/1.0/market/sell-orders?limit={limit}&maxPrice={max_price}&minPrice={min_price}&offset={offset}&order=desc&sort=discount&type=2'
            r = requests.get(url=url, headers={"User-Agent": f'{ua.random}'})
            data = r.json()
            items = data['items']
            offset += limit

            # Parsing JSON
            for item in items:
                if item['pricing']['discount'] > 0.1:
                    title = item['asset']['names']['short']
                    price = item['pricing']['computed']
                    discount = round((item['pricing']['discount'] * 100), 2)
                    try:
                        link = item['links']['3d']
                    except:
                        link = ''
                    result.append({
                        'title': title,
                        'price': price,
                        'discount': discount,
                        'link_3d': link,
                    })
                    count += 1

        pages += 1
        print(f'Page #{pages}')
        print(f'{url}')

        if len(items) < 60:
            break

    # Запись JSON
    with open('data.json', 'w+') as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)

    print(f"[INFO] Items found: {count}")

    # exit()

    # Parsing HTML
    #     file = open(f"html/data_{i}.html", "r", encoding='utf8')
    #     soup = BeautifulSoup(file, 'lxml')
    #     shoes = soup.find('div', id='comjshop_list_product').find_all('div', class_='block_product')
    #     for item in shoes:
    #         title = item.find('div', class_='name').find('a').text.strip()
    #         price = item.find('div', class_='jshop_price').find('span').text.strip()
    #         image = item.find('img', class_='jshop_img').get('src').strip()
    #         link = item.find('div', class_='image_block').find('a').get('href').strip()
    #         total += 1
    #         result_data.append({
    #             'title': title,
    #             'price': price,
    #             'image': image,
    #             'link': "https://salomon.kz/" + link,
    #         })
    #         # print(title, price, image)
    # print(f'[+] Scraping done, find total={total}')
    # with open('data.json', 'w') as json_file:
    #     json.dump(result_data, json_file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
