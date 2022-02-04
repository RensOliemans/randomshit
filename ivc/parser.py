import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread('index.jpg')

d = pytesseract.image_to_data(img, output_type=Output.DICT)

print(d['text'])
