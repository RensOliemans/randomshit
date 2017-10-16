import random
import sys
import getopt
import os


def is_het_getal(dobbelstenen=1, getal=6):
    worp = 0
    for _ in range(dobbelstenen):
        worp += random.randrange(1, 7)
    return worp == getal


def get_args(argv):
    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} -w <worpen> -d <dobbelstenen> " \
                   "-g <getal>".format(program_file)

    # default values
    worpen = 10000
    dobbelstenen = 2
    getal = 6

    try:
        opts, args = getopt.getopt(argv, "w:d:g:")
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            sys.exit()
        elif opt == "-w":
            worpen = int(arg)
        elif opt == "-d":
            dobbelstenen = int(arg)
        elif opt == "-g":
            getal = int(arg)

    return (worpen, dobbelstenen, getal)


if __name__ == "__main__":
    (worpen, dobbelstenen, getal) = get_args(argv=sys.argv[1:])
    for x in range(dobbelstenen):
        zessen = 0
        for _ in range(worpen):
            if is_het_getal(dobbelstenen=x + 1, getal=getal):
                zessen += 1
        print("Met {} dobbelstenen: {}. Kans: {}%".format(
            x + 1, zessen, (zessen / worpen) * 100))
