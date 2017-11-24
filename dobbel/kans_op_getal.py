import random
import sys
import getopt
import os
import time


def is_het_getal(dobbelstenen=1, getal=6):
    worp = 0
    for _ in range(dobbelstenen):
        worp += random.randrange(1, 7)
    return worp == getal


def get_args(argv):
    program_file = os.path.basename(__file__)
    usage_string = "Usage: python3 {} -w <worpen> -d <dobbelstenen> " \
                   "-g <getal> [-t] [-h] [-e]".format(program_file)
    help_string = usage_string + "\n" + "-t: time the program\n" + \
                                        "-a: disable all results (faster)\n" + \
                                        "-h: this help screen"

    # default values
    worpen = 10000
    dobbelstenen = 5
    getal = 12
    timeit = False
    all_results = True

    try:
        opts, args = getopt.getopt(argv, "w:d:g:tha")
    except getopt.GetoptError as e:
        print(usage_string)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(help_string)
            sys.exit()
        elif opt == "-w":
            worpen = int(arg)
        elif opt == "-d":
            dobbelstenen = int(arg)
        elif opt == "-g":
            getal = int(arg)
        elif opt == "-t":
            timeit = True
        elif opt == "-a":
            all_results = False

    print("Instellingen: {} worpen met {} dobbelstenen, het doel is om {} te gooien"
          .format(worpen, dobbelstenen, getal))
    return (worpen, dobbelstenen, getal, timeit, all_results)


def play(worpen, dobbelstenen, getal, timeit):
    start = time.time()
    result = ""
    raak = 0
    for _ in range(worpen):
        if is_het_getal(dobbelstenen=dobbelstenen, getal=getal):
            raak += 1
    result += "Met {} dobbelstenen: {}.\tKans op {}: {:.2%}. ".format(
                   dobbelstenen, raak, getal, (raak / worpen))
    if timeit:
        result += "Job took {} seconds.".format(time.time() - start)
    return result


if __name__ == "__main__":
    (worpen, dobbelstenen, getal, timeit, all_results) = get_args(argv=sys.argv[1:])
    if all_results:
        for x in range(dobbelstenen):
            result = play(worpen, x + 1, getal, timeit)
            print(result)
    else:
        result = play(worpen, dobbelstenen, getal, timeit)
        print(result)
