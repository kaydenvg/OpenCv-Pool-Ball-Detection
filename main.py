import cv2.cv2

from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *

FILES = ['table1.png', 'table2.png', 'IMG_1290.JPG', 'IMG_1291.JPG', 'IMG_1292.JPG', 'IMG_1293.JPG', 'IMG_1294.JPG',
         'IMG_1295.JPG']

if __name__ == '__main__':
    file = "images/" + FILES[2]
    img = cv2.imread(file)
    flat = Houghwarp(setCorners(img), img)

    foundballs = findBalls(flat)

    print("Found ", str(len(foundballs)), " balls: ")

    for team, color, stat, centroid in foundballs:
        print(team, color, stat, centroid)

    # hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV)
    # colorPicker(hsv)
