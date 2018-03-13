import os

KEYBOARD_QWERTY = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
]
KEYBOARD_DVORAK = [
    ["'", ',', '.', 'P', 'Y', 'F', 'G', 'C', 'R', 'L'],
    ['A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S'],
    [';', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z']
]
KEYBOARD_COLEMAK = [
    ['Q', 'W', 'F', 'P', 'G', 'J', 'L', 'U', 'Y', ';'],
    ['A', 'R', 'S', 'T', 'D', 'H', 'N', 'E', 'I', 'O'],
    ['Z', 'X', 'C', 'V', 'B', 'K', 'M', ',', '.', '/']
]
KEYBOARD_WORKMAN = [
    ['Q', 'D', 'R', 'W', 'B', 'J', 'F', 'U', 'P', ';'],
    ['A', 'S', 'H', 'T', 'G', 'Y', 'N', 'E', 'O', 'I'],
    ['Z', 'X', 'M', 'C', 'V', 'K', 'L', ',', '.', '/']
]


def get_movements(keyboard):
    """
    This method gets a keyboard and returns a dictionary with the following
    mapping:

    character: movement_cost

    character is a character that can be found on the keyboard,
    movement_cost is the cost of moving your finger to that character.
    In Qwerty for example, the character 'D' has a cost of 0, since you don't
    have to move your fingers from the home row. The character 'E' has a cost
    of 1, since you have to move your finger one key. The character 'B', f.e.,
    has a cost of 2, because you have to move your finger downwards and to the
    right. (In general, the 'middle' characters of any row have an extra cost).
    This does mean, however that the (Qwerty) key 'N' has a cost of 2 as well,
    but this can be argued against.
    """

    # Movement mapping
    # Middle keys (in Qwerty for example 'G' and 'H') take extra movement
    # top row
    movement_t = {x: 2 if x in keyboard[0][4:6] else 1 for x in keyboard[0]}
    # middle row
    movement_m = {x: 1 if x in keyboard[1][4:6] else 0 for x in keyboard[1]}
    # bottom row
    movement_b = {x: 2 if x in keyboard[2][4:6] else 1 for x in keyboard[2]}

    # create a single dictionary with movements of entire keyboard
    movements = dict()
    movements.update(movement_t)
    movements.update(movement_m)
    movements.update(movement_b)

    return movements


def distance(word, movements):
    """
    This method takes a word and movement mapping (see get_movements())
    as input and returns the 'cost' of moving your fingers in order to type
    the word
    """
    distance = 0
    prev_letter = None
    for letter in word:
        letter = letter.upper()
        if prev_letter is None or not prev_letter == letter:
            # the letter is another letter than the previous one,
            # so increase distance
            try:
                distance += movements[letter]
            except KeyError:
                # key isn't in regular alphabet (number or punctuation prob)
                # just skip
                pass
        prev_letter = letter
    return distance


def distances(words, movements):
    """
    This method takes a list of words as input and a movement mapping
    (see get_movements()) and returns a dictionary distances, with key, value:

    { word: movement_cost }
    """
    distances = dict()
    for word in words:
        distances[word] = distance(word, movements)
    return distances


def dic_to_words(filename):
    with open(filename) as f:
        return [word.split('/')[0] for word in f]


def calculate_avg_moving(words, keyboard):
    movements = get_movements(keyboard)
    dists = distances(words, movements)
    return sum(dists.values()) / len(dists)


def show_movings(words):
    qwerty = calculate_avg_moving(words, KEYBOARD_QWERTY)
    print("Qwerty\taverage moving distance:\t{:.2f}"
          .format(qwerty))

    dvorak = calculate_avg_moving(words, KEYBOARD_DVORAK)
    print("Dvorak\taverage moving distance:\t{:.2f}"
          .format(dvorak))

    colemak = calculate_avg_moving(words, KEYBOARD_COLEMAK)
    print("Colemak\taverage moving distance:\t{:.2f}"
          .format(colemak))

    workman = calculate_avg_moving(words, KEYBOARD_WORKMAN)
    print("Workman\taverage moving distance:\t{:.2f}"
          .format(workman))


def main():
    dict_dir_name = '/home/rens/Projects/randomshit/Dictionaries/'
    dictionaries = [dic for dic in os.listdir(dict_dir_name)
                    if dic[-4:] == '.dic']
    # only dutch
    dictionaries = ['English (British).dic', 'Dutch.dic']

    for dictionary in dictionaries:
        dictionary = dict_dir_name + dictionary
        print("Using dictionary {}".format(dictionary))
        words = dic_to_words(dictionary)
        show_movings(words)


if __name__ == "__main__":
    main()
