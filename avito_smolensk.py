import requests
from bs4 import BeautifulSoup
import csv


def main():
    url = 'https://www.avito.ru/smolensk/kvartiry/prodam?p=1&view=list'
    base_url = 'https://www.avito.ru/smolensk/kvartiry/prodam?'
    page_part = 'p='
    query_part = '&view=list'
    total_pages = get_total_pages(get_html(url))
    for i in range(total_pages+1):
    # for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)

        
def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('smolensk.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['price'],
                         data['area'],
                         data['address']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_list')
    for ad in ads:
        try:
            price = int(ad.find('div', class_='price').find('p').text.strip().strip('\\xa0р.').strip().replace(' ', ''))
        except:
            price = ''

        try:
            area = float(ad.find('div', class_='param area').text.split(' ')[0])
        except:
            area = ''

        try:
            address = ad.find('div', class_='param address').find('div', class_='fader').text.strip()
        except:
            address = ''

        data = {'price': price,
                'area': area,
                'address': address}
        write_csv(data)


if __name__ == '__main__':
    main()
