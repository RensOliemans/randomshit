import os
# import pandas as pd
from objects import CSV, csv_to_transaction


CWD = os.getcwd()
CSV_D = os.pardir + '/' + 'csv' + '/' + '2017' + '/'
try:
    CSV_FILES = os.listdir(CSV_D)
except FileNotFoundError:
    raise FileNotFoundError("Make a directory called 'csv'"
                            " in which you put the csv files")


def convert_csv_to_excel(csv_file):
    pass


def parse_file(filename):
    """
    Takes a csv file (ASN format) as input and returns a
    list of Transaction objects
    """
    transactions = list()
    with open(CSV_D + filename) as f:
        for line in f:
            csv_object = CSV(line)
            transaction = csv_to_transaction(csv_object)
            transactions.append(transaction)
    return transactions


def get_category(transaction, categories):
    if categories:
        print("\nPossible categories: {}".format(", ".join(categories)))
    category = input("What category belongs to this transaction {}?\n"
                     .format(transaction))
    return category


def parse_transactions(transactions, category_filename):
    categories = list()
    with open('categories') as f:
        for line in f:
            categories.append(line)
    category_transactions = dict()
    try:
        for transaction in transactions:
            category = get_category(transaction, categories)
            with open('categories', '+w') as f:
                if category not in categories:
                    categories.append(category)
                f.write('; '.join(categories))
            category_transactions[category] = transaction
    except KeyboardInterrupt:
        return category_transactions
    return category_transactions


def get_month():
    return input("What month do you want?\n") + '.csv'


def choose():
    options = ['categorise', 'edit_cat']
    option = input("What do you want to do?\n")
    if option in options:
        return option
    return 'categorise'


def edit_cat():
    pass


def main():
    month_filename = get_month()
    choice = choose()
    if choice == 'categorise':
        transactions = parse_file(month_filename)
        print(parse_transactions(transactions, 'categories'))
    elif choice == 'edit_cat':
        edit_cat()
