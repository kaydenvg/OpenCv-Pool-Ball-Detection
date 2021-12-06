import cv2.cv2

from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *
from findShot import *

if __name__ == '__main__':
    file = 'images/IMG_1292.JPG'
    img = cv2.imread(file)
    flat = Houghwarp(setCorners(img), img)

    foundballs = findBalls(flat)
    # colorPicker(flat)

    print("Found ", str(len(foundballs)), " balls: ")

    for team, color, stat, center in foundballs:
        print(team, color, center)

    lines1, lines2, angles, distances = getAllShots(flat, 0, foundballs)
    bestshot = getBestShot(flat, lines1, lines2, angles, distances)
    create_named_window("best", bestshot)
    cv2.imshow("best", bestshot)
    cv2.waitKey(0)

