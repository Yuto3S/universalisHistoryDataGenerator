import requests
from bs4 import BeautifulSoup

LODESTONE_PAGE_URL = "https://eu.finalfantasyxiv.com/lodestone/playguide/db/item/?page="


def get_lodestone_items_number_of_pages():
    response = requests.get(f"{LODESTONE_PAGE_URL}")
    soup = BeautifulSoup(response.content, features="html.parser")
    number_of_pages = soup.find("a", {"rel": "last"})["href"].split("?page=")[1]
    return int(number_of_pages)


# Inspired from https://github.com/Asvel/ffxiv-lodestone-item-id/tree/master
def get_lodestone_items_for_page(page):
    items_name_to_lodestoneid = {}

    response = requests.get(f"{LODESTONE_PAGE_URL}{page}")
    if response.status_code != 200:
        print(f"ERROR FOR {page}, {response.status_code}")

    soup = BeautifulSoup(response.content, features="html.parser")
    lodestone_item_links_in_page = soup.find_all(
        "a", {"class": "db-table__txt--detail_link"}
    )

    for item in lodestone_item_links_in_page:
        items_name_to_lodestoneid[item.text] = item["href"][-12:-1]

    return items_name_to_lodestoneid
