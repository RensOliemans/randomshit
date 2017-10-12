import random


def is_het_zes(dobbelstenen=1):
    worp = 0
    for _ in range(dobbelstenen):
        worp += random.randrange(1, 7)
    return worp == 6


if __name__ == "__main__":
    worpen = 3600
    hoeveelheid_zessen_1 = 0
    hoeveelheid_zessen_2 = 0
    for _ in range(worpen):
        if is_het_zes(dobbelstenen=1):
            hoeveelheid_zessen_1 += 1
        if is_het_zes(dobbelstenen=2):
            hoeveelheid_zessen_2 += 1
    print("Met 1 dobbelsteen: {}. Kans: {}.\n"
          "Met 2 dobbelstenen: {}. Kans: {}".format(
              hoeveelheid_zessen_1, hoeveelheid_zessen_1 / worpen,
              hoeveelheid_zessen_2, hoeveelheid_zessen_2 / worpen))
