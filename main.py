import cv2.cv2

from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *
from findShot import *

if __name__ == '__main__':
    file = 'table2.png'
    img = cv2.imread(file)

   # ortho = flattenImage(img)

    flat = Houghwarp(setCorners(img), img)

    foundballs = findBalls(flat)

    print("Found ", str(len(foundballs)), " balls: ")

    for team ,color,stat in foundballs:
        print(team, color, stat)


    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # colorPicker(hsv)
