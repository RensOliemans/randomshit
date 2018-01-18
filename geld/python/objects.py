""" Example line:
02-01-2017,NL66ASNB0707971934,NL73RABO0312903960,woningstichting de
veste,,,,EUR,861.37,EUR,-336.91,02-01-2017,02-01-2017,9714,INC,40740934,,'Europese
incasso door:WONINGSTICHTING DE VESTE NL-Periode: 01-2 """


class CSV(object):

    """This class represents a single csv line"""

    def __init__(self, csv_line):
        self.entries = self.parse_line(csv_line)

    def parse_line(self, csv_line):
        entries = csv_line.split(',')
        parsed_dict = dict()
        parsed_dict['date'] = entries[0]
        parsed_dict['own_iban'] = entries[1]
        parsed_dict['dest_iban'] = entries[2]
        parsed_dict['dest_name'] = entries[3]
        parsed_dict['address'] = entries[4]  # asn doesn't use this fiel
        parsed_dict['zip_code'] = entries[5]  # asn doesn't use this fiel
        parsed_dict['city'] = entries[6]  # asn doesn't use this fiel
        parsed_dict['currency_self'] = entries[7]
        parsed_dict['balance_pre_mut'] = entries[8]
        parsed_dict['currency_mut'] = entries[9]
        parsed_dict['transaction_amount'] = entries[10]
        # this is the date when a transaction has been entered in the asn
        # database
        parsed_dict['journal_date'] = entries[11]
        # valuta_date, the date when a date becomes 'interest-bearing'
        parsed_dict['valuta_date'] = entries[12]
        # internal code for asn, not used here
        parsed_dict['internal_transaction_code'] = entries[13]
        # global transaction codes
        parsed_dict['global_transaction_code'] = entries[14]
        # 'volgnummer transactie', forms a unique id together with journal_date
        # useless
        parsed_dict['volgnummer_transactie'] = entries[15]
        # contains things that are possibly useful for more financial people
        # useless
        parsed_dict['betalingskenmerk'] = entries[16]
        parsed_dict['description'] = entries[17]
        # 'afschrifnummer', nummer of the copy where the transaction was
        # mentioned (not sure how this works in english??)
        parsed_dict['afschriftnummer'] = entries[18]
        return parsed_dict


class Transaction(object):

    """Class for transaction. Contains the useful objects that
    can be found in an ASN CSV file"""

    def __init__(self, date, own_iban, dest_iban, dest_name,
                 amount, description):
        """

        :date: date of the transaction
        :own_iban: IBAN of own account
        :dest_iban: IBAN of the other account in the transaction
        :dest_name: name of the other account in the transaction
        :amount: amount of the transaction
        :description: description of the transaction

        """
        self.date = date
        self.own_iban = own_iban
        self.dest_iban = dest_iban
        self.dest_name = dest_name
        self.amount = amount
        self.description = description

    def __repr__(self):
        repr_string = ("Transaction. Date: {}. Own IBAN: {}. Destination "
                       "IBAN: {}. Destination name: {}. Amount: {}. "
                       "Description: {}")
        return repr_string.format(self.date, self.own_iban, self.dest_iban,
                                  self.dest_name, self.amount,
                                  self.description)

    def __str__(self):
        return "{} from {} on {}, with description: {}".format(
                self.amount, self.dest_name, self.date, self.description)


def csv_to_transaction(csv_object):
    entries = csv_object.entries
    date = entries['date']
    own_iban = entries['own_iban']
    dest_iban = entries['dest_iban']
    dest_name = entries['dest_name']
    amount = entries['transaction_amount']
    description = entries['description']
    trans = Transaction(date, own_iban, dest_iban, dest_name,
                        amount, description)
    return trans
