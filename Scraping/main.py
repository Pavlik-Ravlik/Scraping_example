import json
import time
import requests

from bs4 import BeautifulSoup as Bs
from fake_useragent import UserAgent


BASE_URL = 'https://rezka.ag/'
HEADERS = {'User-Agent': UserAgent().random}


def main():
    list_description = []

    responce = requests.get(url=BASE_URL, headers=HEADERS)
    soup = Bs(responce.content, 'html.parser')
    links = soup.find_all('div', class_='b-content__inline_item-link')
    genres = soup.find_all('div', class_='misc')

    for link, genre in zip(links, genres):
        href = BASE_URL + link.find('a')['href']  # href
        title_href = link.find('a')
        title = title_href.text.strip()  # title
        genre_text = genre.text.split(',')  # list_of_genres
        dict_description = {'title': title,
                            'link': href,
                            'genre': genre_text,
                            }

        list_description.append(dict_description)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(list_description, file, ensure_ascii=False, indent=4)
                


if __name__ == '__main__':
    start_time = time.time()  # Замеряем время перед выполнением функции
    main()
    end_time = time.time()  # Замеряем время после выполнения функции
    execution_time = end_time - start_time  # Рассчитываем время выполнения
    print(f"Время выполнения функции main(): {execution_time} секунд")