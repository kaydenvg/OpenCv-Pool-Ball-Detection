import cv2.cv2

from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *
from findShot import *

if __name__ == '__main__':
    file = 'images/IMG_1290.JPG'
    img = cv2.imread(file)
    flat = Houghwarp(setCorners(img), img)

    foundballs = findBalls(flat)

    print("Found ", str(len(foundballs)), " balls: ")

    for team, color, stat, centroid in foundballs:
        print(team, color, stat, centroid)

    # lines1, lines2, angles = getAllShots(flat, 0, foundballs)
    #
    # bestshot = getBestShot(flat, lines1, lines2, angles)
    # create_named_window("best", bestshot)
    # cv2.imshow("best", bestshot)
    # cv2.waitKey(0)

    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # colorPicker(hsv)
