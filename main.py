import requests
import json
from bs4 import BeautifulSoup


def get_route(page=None):
    """Сборка маршрута для парсинга"""
    domain = 'https://calorizator.ru/product/all'
    if page:
        return f'{domain}?page={page}'
    else:
        return domain


def get_last_page(url):
    """Получаем последнюю страницу"""
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    last_page = soup.find('li', class_='pager-last').text
    last_page = int(last_page)

    return last_page


def float_convert(item):
    """Конвертация формата + проверка на пустоту"""
    if item:
        return float(item)
    else:
        return 0.0


def get_data(row):
    """Сборка словаря с данными для каждого объекта"""
    data_dict = {
        'name': row[1].find('a').text.strip(),
        'protein': float_convert(row[2].text.strip()),
        'fat': float_convert(row[3].text.strip()),
        'carbohydrate': float_convert(row[4].text.strip()),
        'kcal': float_convert(row[5].text.strip())
    }
    return data_dict


def get_product_data(last_page):
    """Сборка всех данных с сайта, сборка в list"""
    all_products_lst = []
    count = 0

    for page in range(last_page):
        print(f'[INFO] Page {page + 1} / {last_page} in progress')
        url = get_route(page)
        
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        rows = soup.find('table').find('tbody').find_all('tr')
        for row in rows:
            data_row = row.find_all('td')
            all_products_lst.append(get_data(data_row))
            count += 1
    print(f'[INFO] Collected {count} items')
    return all_products_lst

def create_json(data):
    """Создание файла с json данными"""
    with open('data_set.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print('[INFO] Task completed. JSON created')
    return


def main():
    last_page = get_last_page(get_route())
    geted_data = get_product_data(last_page)
    create_json(geted_data)


if __name__ == '__main__':
    main()
