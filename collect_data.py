import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
from sqlquery import create_table, new_push_data
import time
import loguru


def collect_data():
    global min_count, max_count
    first_time = time.time()
    urls = 'https://mir-kvestov.ru/quests/'
    r = get(urls)
    soup = bs(r.text, 'lxml')
    b = soup.find_all('li', class_='quest-tile-1')
    simple_list = []
    create_table()
    for i in b:
        try:
            url = 'https://mir-kvestov.ru' + i.find('a', class_='item-hover quest_tile_hover_link').get('href')
        except:
            break
        try:
            age = int(i.find('span', class_='quest-age').text[:-1])
        except:
            age = 0
        try:
            if len(i.find('span', class_='quest-participants-count').text) == 3:
                try:
                    min_count = int(i.find('span', class_='quest-participants-count').text[:1])
                    max_count = int(i.find('span', class_='quest-participants-count').text[2:])
                except:
                    loguru.Message("Это не число")
            elif len(i.find('span', class_='quest-participants-count').text) > 3:
                try:
                    min_count = int(i.find('span', class_='quest-participants-count').text[:2])
                    max_count = int(i.find('span', class_='quest-participants-count').text[3:])
                except:
                    loguru.Message("Это не число")
        except:
            count = 0
        try:
            scary = len(list(i.find('figure').find('a', class_='quest_tile_hover_text_link').
                             find('p', class_='quest_params features').find('span', class_='quest-scary').find_all(
                'img')))
        except:
            scary = 0
        try:
            rating = float(i.find('p', class_='quest_params rating-emoticon').find('span', class_='qt-1_rp_ev').text)
        except:
            rating = 0
        try:
            typs = str(
                i.find('div', class_='item-box-desc quest-tile-1__content').find('span', class_='game-type').text)
        except:
            typs = 'Нет данных'
        try:
            status = str(i.find('div', class_='item-box-desc quest-tile-1__content').find('h4',
                                                                                          class_='quest-tile-1__title').find(
                'span', class_='badge badge-red-dark').text)
            continue
        except:
            status = 'Открыт'
        simple_list.append([age, min_count, max_count, scary, rating, typs, status, url])
    new_push_data(simple_list)
    second_time = time.time()
    print(second_time - first_time)

    headers = ['age', 'min_count', 'max_count', 'scary', 'rating', 'type', 'status', 'url']
    df = pd.DataFrame(simple_list, columns=headers)
    df.to_csv('F://data.csv', mode='w', sep=';', encoding='cp1251')


if __name__ == '__main__':
    collect_data()
