import csv
from collections import namedtuple

DIRECTORY = "csv/2017/"
FILENAME = DIRECTORY + "February.csv"

Entry = namedtuple(
    "Entry",
    "datum rekening1 rekening2 naam_tegen adres postcode plaats valutasoort_rekening saldo valutasoort_mutatie transactiebedrag journaaldatum valutadatum intern globaal volgnummer betalingskenmerk omschrijving afschrifnummer",
)
# Convert = namedtuple('Convert', 'date payment info payee memo amount category tags')
Convert = namedtuple("Convert", "date payee category memo outflow inflow")


def complete(filename):
    items = list()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        items = list(reader)

    entries = [Entry._make([param for param in item] for item in items)]

    with open("output.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for entry in entries:
            writer.writerow([param for param in convert_entry(entry)])


def convert_entry(entry: Entry):
    outflow, inflow = 0, 0
    if entry.transactiebedrag > 0:
        inflow = entry.transactiebedrag
    else:
        outflow = abs(entry.transactiebedrag)
    return Convert(
        entry.datum, entry.naam_tegen, "", entry.omschrijving, outflow, inflow
    )


if __name__ == "__main__":
    complete(FILENAME)
