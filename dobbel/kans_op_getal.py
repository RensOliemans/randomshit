import random
import time
import begin


def is_het_getal(dobbelstenen=1, getal=6):
    worp = 0
    for _ in range(dobbelstenen):
        worp += random.randrange(1, 7)
    return worp == getal


def play(worpen, dobbelstenen, getal, timeit):
    start = time.time()
    result = ""
    raak = 0
    for _ in range(worpen):
        if is_het_getal(dobbelstenen=dobbelstenen, getal=getal):
            raak += 1
    result += "Met {:<2} dobbelstenen: {:<5}\tKans op {}: {:.2%}.".format(
        dobbelstenen, raak, getal, (raak / worpen))
    if timeit:
        result += "\tJob took {:.2} seconds.".format(time.time() - start)
    return result


@begin.start(auto_convert=True)
def main(w: 'worpen' = 10000, d: 'dobbelstenen' = 5, g: 'getal' = 12,
         t: 'time' = True, a: 'disable all results' = True):
    """
    Probeert een getal te gooien met een aantal dobbelstenen, en kijkt
    hoe vaak dat lukt
    """
    print("Instellingen: {} worpen met {} dobbelstenen, het doel is om {}"
          " te gooien".format(w, d, g))

    if a:
        for x in range(d):
            result = play(w, x + 1, g, t)
            print(result)
    else:
        result = play(w, d, g, t)
        print(result)
