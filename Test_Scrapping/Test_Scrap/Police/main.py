import requests
import json
import csv
from bs4 import BeautifulSoup

def all_pages():
    count = 1
    url = f'https://www.police1.com/law-enforcement-directory/search/page-{count}'
    list_of_links = []

    while count < 20:
        try:
            responce = requests.get(url=url)
            soup = BeautifulSoup(responce.content, 'lxml')

            for elem in soup.find_all('a', class_='Table-row'):
                href = elem['href'][1:]
                list_of_links.append(href)
            
            count += 1
        
        except:
            break

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



def main():
    find_func = info()
    save_json = save_to_json(find_func)
    save_csv = save_to_csv(find_func)


if __name__ == '__main__':
    main()
    
