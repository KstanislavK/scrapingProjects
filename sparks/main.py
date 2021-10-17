import csv
import datetime

import requests
from bs4 import BeautifulSoup
import json

domain = "http://www.sparksfilms.ru"


def get_categories(url):
    req = requests.get(url)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    cat_hrefs = soup.find("td", class_="content_block").find_all("a")[2:]

    with open("cat_urls.txt", "w") as file:
        for item in cat_hrefs:
            title = item.text
            excepts = ["АВТОХИМИЯ и АВТОКОСМЕТИКА BULLSONE", "Ремонт автостекол", "Инструменты"]
            if title in excepts:
                continue
            else:
                line = f'http://www.sparksfilms.ru{item.get("href")}\n'
                file.write(line)

    return "cat_urls.txt"


def get_data(file):
    with open(file) as file:
        src = file.readlines()

    for url in src:
        req = requests.get(url)
        src = req.text

        soup = BeautifulSoup(src, "lxml")
        category_title = soup.find("title").text.split("/")[0].strip().replace(" ", "_")

        film_url_list = soup.find_all("table", class_="item_img")

        with open(f"csvs/{category_title}.csv", "w", encoding="windows-1251", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                ("Name", "URL", "Price by meter", "Price by roll")
            )


        all_film_data = []
        for item in film_url_list:
            film_url = f'{domain}{item.find("a").get("href")}'
            film_name = item.find("a").get("title")

            req = requests.get(film_url)
            src_film = req.text

            soup_film = BeautifulSoup(src_film, "lxml")

            try:
                all_prices = soup_film.find_all("p", class_="cost")
                film_price_m = all_prices[0].text.replace('"', "").split()[0].strip()
                film_price_roll = all_prices[1].text.split()[0].strip()
            except:
                film_price_m = None
                film_price_roll = None

            film_dict = {
                "title": film_name,
                "url": film_url,
                "price_m": film_price_m,
                "price_roll": film_price_roll
            }
            all_film_data.append(film_dict)

            with open(f"csvs/{category_title}.csv", "a", encoding="windows-1251", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(
                    (film_name, film_url, film_price_m, film_price_roll)
                )

        with open(f"jsons/{category_title}.json", "a") as file:
            json.dump(all_film_data, file, indent=4, ensure_ascii=False)

        print(f'[INFO] Копирование категории "{category_title}" завершено')


def main():
    url = "http://www.sparksfilms.ru/products.html"
    start_time = datetime.datetime.now()
    file = get_categories(url)
    get_data(file)
    end_time = datetime.datetime.now() - start_time

    print(end_time)


if __name__ == '__main__':
    main()
