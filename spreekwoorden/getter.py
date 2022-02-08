import json
import logging
from urllib import request

from bs4 import BeautifulSoup


URL = "https://spreekwoorden.nl/spreekwoorden-a-z"


def determine_max_pages(url):
    html_page = request.urlopen(url).read()
    soup = BeautifulSoup(html_page, "html.parser")
    page_list = soup.find(attrs={"class": "pagination"})
    # -1 is \n, -2 is next page, -3 is '\n', -4 is last page
    last = list(page_list.children)[-4]
    return int(last.text)


def get_proverbs(url, pages):
    proverbs = dict()
    for page in pages:
        html_page = request.urlopen(url + page).read()
        soup = BeautifulSoup(html_page, "html.parser")
        html_proverbs = soup.find_all(attrs={"class": "proverb-item"})
        for proverb in html_proverbs:
            title = proverb.find(attrs={"class": "proverb-item__heading"}).text.strip()
            meaning = proverb.find(attrs={"class": "proverb-item__body"}).text.strip()
            proverbs[title] = meaning
    return proverbs


def main():
    max_pages = determine_max_pages(URL)
    logging.info("Getting info from %s pages", max_pages)
    pages = [f"?page={x}" for x in range(1, max_pages + 1)]

    proverbs = get_proverbs(URL, pages)

    with open("dump.json", "w") as f:
        json.dump(proverbs, f)


if __name__ == "__main__":
    main()
