import inspect

import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import loguru


def show_kvest_info(url):
    # urls = 'https://mir-kvestov.ru/quests/quest-testament-mortir'
    urls = url
    r = get(urls)
    soup = bs(r.text, 'lxml')
    # print(soup)
    # description = soup.find(attrs={'itemprop': 'description'}).find_all('p')
    description = soup.find(attrs={'itemprop': 'description'}).find_all('p')
    a = [i.contents for i in description]
    # descr_data = []
    descr_data = ''
    for p in list(a):
        for g in p:
            if g.name != 'br':
                descr_data += ''.join(g)
    return descr_data
            # if not g.startwith('<'):
            #     descr_data = ''.join(p)
            #     # s = ''.join(j[0] + j[2])
            #     print(descr_data)
    # print(*a)
    # print(''.join(*a))
    # description = soup.findall('p', class_='description')
    # print(description)
    # headers = ['1', '2', '3', '4', '5', '6', '7']
    # headers = ['1']
    # df = pd.DataFrame(description, columns=headers)
    # df.to_csv('F://kvest_data.csv', mode='w', sep=';', encoding='cp1251')



if __name__ == '__main__':
    show_kvest_info()
