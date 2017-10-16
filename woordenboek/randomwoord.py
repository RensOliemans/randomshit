import random
import io

def get_word(filename="nl_NL.dic"):
    f = io.open(filename, encoding='latin-1')
    words = list()
    for word in f:
        words.append(word)
    f.close()
    word = ""
    # we only want long words
    while len(word) < 10:
        # get random word and remove last character, which is always a whitespace
        word = words[random.randrange(0, len(words))][:-1]
        # occasionally word has /X (X being 1 or more characters) at the end, remove it
        if "/" in word:
            # get index of '/', counting from the back
            index = len(word) - word.index("/")
            word = word[:-index]
    return word

if __name__ == "__main__":
    for _ in range(5):
        print(get_word())
