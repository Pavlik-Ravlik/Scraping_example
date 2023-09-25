import requests
import json
import csv
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def all_pages():
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        count = 1
        tasks = []

        while count < 15:
            url = f'https://www.police1.com/law-enforcement-directory/search/page-{count}'
            responses = await asyncio.gather(*tasks)
            list_of_links = []

            for content in responses:
                soup = BeautifulSoup(content, 'lxml')

                for elem in soup.find_all('a', class_='Table-row'):
                    href = elem['href'][1:]
                    list_of_links.append(href)
            
            return list_of_links




        

        for content in responses:
            soup = BeautifulSoup(content, 'lxml')

            for elem in soup.find_all('a', class_='Table-row'):
                href = elem['href'][1:]
                list_of_links.append(href)
        
        return list_of_links






def info():
    list_of = []
    
    pages = all_pages()
    base_url = 'https://www.police1.com/'
    
    for href in pages:
        responce = requests.get(url=base_url + href)
        soup = BeautifulSoup(responce.content, 'lxml')

        dd = soup.find_all('dd', class_='DefList-description')
        name = soup.find('h1', class_="Article-p Article-p--heading")
        name = name.text.strip()

        list_of.append({'Name': name, 
                        'Address': dd[1].text,
                        'City': dd[2].text, 
                        'State': dd[3].text, 
                        'Zip Code': dd[4].text,
                        'County': dd[5].text, 
                        'Phone': dd[6].text, 
                        })

    return list_of


def save_to_json(list_of):
    with open('files/data.json', 'w', encoding='utf-8') as file:
        a = json.dump(list_of, file, ensure_ascii=False, indent=4)


def save_to_csv(list_of):
    with open('files/data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'City', 'State', 'Zip Code', 'County', 'Phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in list_of:
            writer.writerow(item)



async def main():
    page = await all_pages()


if __name__ == '__main__':
    print(asyncio.run(main()))
