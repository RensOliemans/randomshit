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
COLOR = (138, 66, 29)


def main():
    image, d = parse_image(FILENAME)
    boxes = find_all_boxes(d, TEAM, DIST, EXPECTED_APPEARANCES)
    highlight_boxes(image, boxes, PIXELWIDTH, COLOR)
    output(image, OUTPUT)


def parse_image(filename):
    img = cv2.imread(filename)
    return img, pytesseract.image_to_data(img, output_type=Output.DICT)


def find_all_boxes(data, team, dist, expected):
    boxes = list(find_boxes(data, team, dist))
    while len(boxes) < expected:
        dist += 1
        boxes = list(find_boxes(data, team, dist))

    return boxes


def find_boxes(data, text, dist):
    for i, box in enumerate(data['text']):
        if same(box, text, dist):
            yield data['left'][i], data['top'][i], data['width'][i], data['height'][i]


def highlight_boxes(img, boxes, pixelwidth, color):
    for (x, y, w, h) in boxes:
        x -= pixelwidth
        y -= pixelwidth
        w += 2 * pixelwidth
        h += 2 * pixelwidth
        img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)


def same(found, actual, dist):
    return distance(found.lower(), actual.lower()) < dist


def output(img, filename=None):
    if filename:
        cv2.imwrite(filename, img)
    else:
        cv2.imshow('img', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
