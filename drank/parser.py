"""
This module is made to parse the winkelwagen of drankgigant.nl
"""
import string
from collections import namedtuple

import bs4

FLOATABLE = set(string.digits).union({"."})


Beer = namedtuple("Beer", "name price amount")


def get_items(filename):
    """Returns all cart items, in bs4 elements format."""
    html = open(filename).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup.find_all(attrs={"class": "item-info"})


def get_names(items):
    """Gets the beer names of bs4 elements."""
    product_names = items[0].find_all_next(attrs={"class": "product-item-name"})
    return [product.text.replace("\n", "") for product in product_names]


def get_prices(items):
    """Gets the prices of bs4 elements."""
    products_with_prices = items[0].find_all_next(attrs={"class": "cart-price"})
    # the odd prices are intermediate prices in the html page, we don't need them
    products_with_prices = [
        product
        for product in products_with_prices
        if products_with_prices.index(product) % 2 == 0
    ]
    # convert to floats: only have digits and '.' (replace the ','s though)
    prices = [
        float("".join(filter(lambda x: x in FLOATABLE, product.text.replace(",", "."))))
        for product in products_with_prices
    ]
    return prices


def get_amounts(items):
    """Gets the amounts of bs4 elements."""
    product_amount = items[0].find_all_next(attrs={"class": "control qty"})
    return [int(product.input.attrs["value"]) for product in product_amount]


def main():
    """Main method."""
    all_items = get_items("Winkelwagen | Drankgigant.nl.html")
    names, prices, amounts = (
        get_names(all_items),
        get_prices(all_items),
        get_amounts(all_items),
    )
    print(
        *[
            Beer(name=name, price=price, amount=amount)
            for name, price, amount in list(zip(names, prices, amounts))
        ],
        sep="\n"
    )


if __name__ == "__main__":
    main()
