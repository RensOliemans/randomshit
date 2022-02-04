import cv2
import pytesseract
from pytesseract import Output

FILENAME = 'index.jpg'
TEAM = 'Inter-Actief'
PIXELWIDTH = 5

img = cv2.imread('index.jpg')

d = pytesseract.image_to_data(img, output_type=Output.DICT)

for i, box in enumerate(d['text']):
    if box == 'Inter-Actief':
        (x, y, w, h) = (d['left'][i] - PIXELWIDTH, d['top'][i] - PIXELWIDTH,
                        d['width'][i] + 2 * PIXELWIDTH, d['height'][i] + 2 * PIXELWIDTH)
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        found = True

cv2.imwrite('output.jpg', img)
