import cv2
import pytesseract
from pytesseract import Output

FILENAME = 'index.jpg'
OUTPUT = 'output.jpg'
TEAM = 'Inter-Actief'
PIXELWIDTH = 5


def parse_image(filename):
    img = cv2.imread(filename)
    return img, pytesseract.image_to_data(img, output_type=Output.DICT)


def highlight_boxes(img, data, text, pixelwidth):
    for i, box in enumerate(data['text']):
        if box == text:
            (x, y, w, h) = (data['left'][i] - pixelwidth, data['top'][i] - pixelwidth,
                            data['width'][i] + 2 * pixelwidth, data['height'][i] + 2 * pixelwidth)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return img


def output(img, filename=None):
    if filename:
        cv2.imwrite(filename, img)
    else:
        cv2.imshow('img', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    img, data = parse_image(FILENAME)
    img = highlight_boxes(img, data, TEAM, PIXELWIDTH)
    output(img, OUTPUT)
