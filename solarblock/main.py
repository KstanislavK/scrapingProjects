import csv
import datetime
import time

import requests
from bs4 import BeautifulSoup
import json

domain = 'https://www.solarblock.ru'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
}


def get_pages(domain):
    req = requests.get(domain)
    src = req.text

    soup = BeautifulSoup(src, "lxml")
    categories_list = []
    category_li = soup.find("ul", class_="nav-tabs").find_all("li")
    for item in category_li:
        link = item.find("a").get("href")
        full_link = f"{domain}{link}"
        categories_list.append(full_link)

    return categories_list


def get_data(url_list, headers):
    for url in url_list:
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        category_title = soup.find("h1", class_="protect__title").text.strip()

        with open(f"csvs/{category_title}.csv", "w",  encoding="windows-1251", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(("Name", "Link", "Articul", "VLT", "Meter_cost", "Roll_cost"))

        tr_list = soup.find("tbody").find_all("tr")
        data = []
        for item in tr_list:
            td_list = item.find_all("td")

            if len(td_list) <= 1:
                continue
            else:
                film_link = f'{domain}{td_list[1].find("a").get("href")}'
                film_name = td_list[1].find("a").find("span").text.strip()
                film_art = td_list[1].text.split("\n\n")[2].strip()
                film_vlt = td_list[3].text.strip()
                film_cost_roll = td_list[4].text.replace("\u20bd", "").strip()
                film_cost_meter = td_list[5].text.replace("\u20bd", "").strip()

                data_dict = {
                    "film_name": film_name,
                    "film_link": film_link,
                    "film_articul": film_art,
                    "film_VLT": film_vlt,
                    "price_meter": film_cost_meter,
                    "price_roll": film_cost_roll
                }

            with open(f"csvs/{category_title}.csv", "a", encoding="windows-1251", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow((film_name, film_link, film_art, film_vlt, film_cost_meter, film_cost_roll))

            data.append(data_dict)
        with open(f"jsons/{category_title}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"[INFO] Раздел '{category_title}' скачан")
        time.sleep(1)


def main():
    start_time = datetime.datetime.now()
    url_list = get_pages(domain)
    get_data(url_list, headers)
    end_time = datetime.datetime.now() - start_time
    print(f"Spent time: {end_time}")


if __name__ == '__main__':
    main()
