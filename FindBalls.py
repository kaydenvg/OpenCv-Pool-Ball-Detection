import cv2
import numpy as np
from miscFunctions import *

def nothing(x):
    pass

def setImageThresholds():
    # set thresholds
    low_thresholds = [0, 0, 0]
    high_thresholds = [255, 255, 255]

    #import image, convert to hsv
    filename = str(input("enter a file name:"))
    bgr_img = cv2.imread(filename)
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    image_height = bgr_img.shape[0]
    image_width = bgr_img.shape[1]

    # Split into the different bands.
    planes = cv2.split(hsv_img)
    windowNames = ["Hue image", "Saturation image", "Gray image"]
    for i in range(3):
        create_named_window(windowNames[i], hsv_img)
    for i in range(3):
        cv2.createTrackbar("Low", windowNames[i], low_thresholds[i], 255, nothing)
        cv2.createTrackbar("High", windowNames[i], high_thresholds[i], 255, nothing)


    while True:
        # Create output thresholded image.
        thresh_img = np.full((image_height, image_width), 255, dtype=np.uint8)
        for i in range(3):
            low_val = cv2.getTrackbarPos("Low", windowNames[i])
            high_val = cv2.getTrackbarPos("High", windowNames[i])

            _, low_img = cv2.threshold(planes[i], low_val, 255, cv2.THRESH_BINARY)
            _, high_img = cv2.threshold(planes[i], high_val, 255, cv2.THRESH_BINARY_INV)

            thresh_band_img = cv2.bitwise_and(low_img, high_img)
            cv2.imshow(windowNames[i], thresh_band_img)

            # AND with output thresholded image.
            thresh_img = cv2.bitwise_and(thresh_img, thresh_band_img)

        create_named_window("Output thresholded image", thresh_img)
        cv2.imshow("Output thresholded image", thresh_img)
        if not cv2.waitKey(100) == -1:
            break

def findBalls(filename):
    colorlist = []
    colorPicker(filename, colorlist=colorlist)
    print(colorlist)
    img = cv2.imread(filename)
    # color_thresh = int(input("Input color thresh: "))
    hsv = cv2.cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    lower_range = np.array([230, 85, 60]) #TODO: loop through all colored balls, currently only orange
    upper_range = np.array([255, 120, 75])

    print(lower_range, upper_range)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    create_named_window("img", img)
    cv2.imshow("img", img)
    create_named_window("mask", mask)
    cv2.imshow("mask", mask)
    cv2.waitKey(0)