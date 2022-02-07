import cv2
import pytesseract
from pytesseract import Output
from Levenshtein import distance

FILENAME = 'index.jpg'
OUTPUT = 'output.jpg'
TEAM = 'Inter-Actief'

PIXELWIDTH = 5
DIST = 3
EXPECTED_APPEARANCES = 7


def parse_image(filename):
    img = cv2.imread(filename)
    return img, pytesseract.image_to_data(img, output_type=Output.DICT)


def find_boxes(image, data, team, pixelwidth, dist, expected):
    n = highlight_boxes(image, d, team, pixelwidth, dist)
    while n < expected:
        dist += 1
        n = highlight_boxes(image, d, team, pixelwidth, dist)


def highlight_boxes(img, data, text, pixelwidth, dist=5):
    n = 0
    for i, box in enumerate(data['text']):
        if same(box, text, dist):
            (x, y, w, h) = (data['left'][i] - pixelwidth, data['top'][i] - pixelwidth,
                            data['width'][i] + 2 * pixelwidth, data['height'][i] + 2 * pixelwidth)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            n += 1

    return n


def same(found, actual, dist):
    return distance(found.lower(), actual.lower()) < dist


def output(img, filename=None):
    if filename:
        cv2.imwrite(filename, img)
    else:
        cv2.imshow('img', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    image, d = parse_image(FILENAME)
    find_boxes(image, d, TEAM, PIXELWIDTH, DIST, EXPECTED_APPEARANCES)
    output(image, OUTPUT)
