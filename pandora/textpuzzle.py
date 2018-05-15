import periodictable as pt
import requests
import json
text = "Once upon a time there was a doctor. Her name was Margaret and the last name resembled german death. That day was a sunday and she didnt have to go to work so she decided to continue writing her first, yet to be published book. Its title was something about escaping and it began with such words: It was a bitter December night, but the Paris-lyon express was speeding gaily along in search of the flowers and the sunshine. After some time passed she decided to go out. She was surprised to meet an old family friend of hers. They talked for a while and exchanged some ideas. Frederick had discovered something but was unsure how to name it and Margaret helped him. He normally was a very stable man and did not break down but it was visible that he really liked the name. After this encounter Margaret decided to call it a day."

with open('isotopes') as f:
    elements = json.load(f)


# returned waarde van een element
# Dit werkt niet, omdat ik niet snap hoe ze de waardes van elementen vinden
def evalue(el):
    # parse element zodat de eerste letter een hoofdletter is
    el = list(el)
    el[0] = el[0].upper()
    el = "".join(el)
    # als element bestaat, zoeken we de naam op en kijken we op wikipedia hoeveel stabiele isotopen er zijn
    if el in [x.symbol for x in pt.elements]:
        e = pt.elements.__getattribute__(el)
        try:
            return elements[e.name]
        except KeyError:
            tt = requests.get("https://en.wikipedia.org/wiki/Isotopes_of_%s" % e.name).text
            return tt.count("<b>Stable</b>")
    else:
        return 0


# Returned waarde van een woord. Dit werkt vrij zeker
def wvalue(word, debug=True):
    res = 0
    i = 0
    while i < len(word):
        if i == len(word)-1:
            if debug:
                print("returning %i + last char of %i" % (res, evalue(word[i])))
            return res + evalue(word[i])
        if evalue(word[i:i+2]) > 0:
            if debug:
                print("%s is value %i" % (word[i:i+2], evalue(word[i:i+2])))
            res += evalue(word[i:i+2])
            i += 2
            continue
        else:
            if evalue(word[i]) > 0 and debug:
                print("%s is value %i" % (word[i], evalue(word[i])))
            res += evalue(word[i])
            i += 1
    return res


# Berekent waarde van een zin door de functies hier boven te werken.. Dit werkt vast ook wel
def svalue(sentence):
    sentence = sentence.split(" ")
    sign = 1
    res = 0
    for w in sentence:
        v = wvalue(w, False)
        print("%s has value %i and sign %i" % (w, v, sign))
        res += v*sign
        sign *= -1
    return res


if __name__ == '__main__':
    print(svalue(text))
