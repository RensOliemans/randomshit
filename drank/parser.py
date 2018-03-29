"""
This module is made to parse the winkelwagen of drankgigant.nl
"""
import string
from collections import namedtuple

import bs4

PRINTABLE = set(string.printable)


Beer = namedtuple('Beer', 'name price amount')


def get_items(filename):
    """ Returns all cart items, in bs4 elements format. """
    html = open(filename).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.find_all(attrs={'class': 'item-info'})


def get_names(items):
    """ Gets the beer names of bs4 elements. """
    product_names = items[0].find_all_next(attrs={'class': 'product-item-name'})
    names = list()
    for product in product_names:
        names.append(product.text.replace('\n', ''))
    return names


def get_prices(items):
    """ Gets the prices of bs4 elements. """
    product_prices = items[0].find_all_next(attrs={'class': 'cart-price'})
    prices = list()
    counter = 0
    for product in product_prices:
        counter += 1
        if counter % 2 == 0:
            continue
        text = ''.join(filter(lambda x: x in PRINTABLE, product.text))
        text = float(text.replace('\n', '').replace(',', '.'))
        prices.append(text)
    return prices


def get_amount(items):
    """ Gets the amounts of bs4 elements. """
    product_amount = items[0].find_all_next(attrs={'class': 'control qty'})
    amounts = list()
    for product in product_amount:
        amounts.append(int(product.input.attrs['value']))
    return amounts


def main():
    """ Main method. """
    items = get_items('Winkelwagen | Drankgigant.nl.html')
    names, prices, values = get_names(items), get_prices(items), get_amount(items)
    beer_items = list(zip(names, prices, values))
    beers = list()
    for beer_item in beer_items:
        beer = Beer(name=beer_item[0], price=beer_item[1], amount=beer_item[2])
        beers.append(beer)
    print(*beers, sep='\n')


if __name__ == "__main__":
    main()
