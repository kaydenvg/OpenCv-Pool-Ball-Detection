import cv2.cv2
import numpy as np

from imports import *
from miscFunctions import *


def setImageThresholds(img):
    # set HSV thresholds HUE:0-179 | SATURATION/VALUE:0-255
    low_thresholds = [0, 0, 0]
    high_thresholds = [179, 255, 255]

    bgr_img = img

    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    image_height = bgr_img.shape[0]
    image_width = bgr_img.shape[1]

    cv2.imshow("image", cv2.resize(bgr_img, dsize=(image_width // 3, image_height // 3)))

    # Split into the different bands.
    planes = cv2.split(hsv_img)
    windowNames = ["Hue image", "Saturation image", "Gray image"]
    for i in range(3):
        create_named_window(windowNames[i], hsv_img)
    for i in range(3):
        cv2.createTrackbar("Low", windowNames[i], low_thresholds[i], high_thresholds[i], nothing)
        cv2.createTrackbar("High", windowNames[i], high_thresholds[i], high_thresholds[i], nothing)

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


def colorHist(img):
    h, s, v = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    hist_h = cv2.calcHist([h], [0], None, [179], [0, 179])
    hist_s = cv2.calcHist([s], [0], None, [256], [0, 256])
    hist_v = cv2.calcHist([v], [0], None, [256], [0, 256])
    plt.plot(hist_h, color='r', label="h")
    plt.plot(hist_s, color='b', label="s")
    plt.plot(hist_v, color='g', label="v")
    plt.legend()
    plt.show()


def findCirlces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (1, 1))

    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 40, param1=20, param2=50, minRadius=42, maxRadius=45)

    # Draw circles that are detected.
    if circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            create_named_window("Detected Circle", img)
            cv2.imshow("Detected Circle", img)
            cv2.waitKey(0)


def getHueOfTable(img):
    # takes hsv img
    h, s, v = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    hist_h = cv2.calcHist([h], [0], None, [179], [0, 179])
    hval = np.argmax(hist_h)
    # print('table hue: ', hval)

    hist_h = np.delete(hist_h, range(hval - 10, hval + 10))
    hval2 = np.argmax(hist_h)
    # print('secondLargestHue:', hval2)

    return hval, hval2


def findBalls(img):
    """
    Finds each color of pool ball in an image file

    :param filename: image file name - string

    return list [ tuple (colorname, ballstats) ]
    """

    height, width, _ = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # colorHist(hsv)

    # remove table
    hueTable, hueTableMaterial = getHueOfTable(hsv)
    lower = (int(hueTable - 3), 0, 0)
    upper = (int(hueTable + 3), 255, 255)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_not(mask)
    # lower = (int(hueTableMaterial - 2), 0, 0)
    # upper = (int(hueTableMaterial + 2), 255, 255)
    # mask = cv2.inRange(hsv, lower, upper)
    # mask = cv2.bitwise_not(mask)

    ksize = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ksize = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
    table = cv2.bitwise_and(img, img, mask=mask)

    create_named_window("Table mask", table)
    cv2.imshow("Table mask", table)
    cv2.waitKey(0)

    found_balls = []

    # Poolball color values
    # TODO: adaptive thresholding
    colorlist = ['yellow', 'blue', 'red', 'purple', 'orange', 'green', 'burgundy', 'black', 'white']
    hue_ranges = [(15, 35), (105, 120), (0, 5), (120, 130), (5, 10), (60, 90), (176, 179), (90, 179), (10, 40)]
    sat_ranges = [(150, 255), (0, 255), (138, 255), (70, 125), (170, 210), (43, 255), (100, 160), (0, 200), (50, 200)]
    val_ranges = [(150, 255), (60, 255), (200, 255), (80, 255), (220, 255), (37, 150), (100, 255), (1, 50), (170, 255)]

    for i in range(len(colorlist)):
        hLow, hHigh = hue_ranges[i]
        sLow, sHigh = sat_ranges[i]
        vLow, vHigh = val_ranges[i]

        lower = (hLow, sLow, vLow)
        upper = (hHigh, sHigh, vHigh)

        # print(colorlist[i] + ' threshold: L=', lower, ' H=', upper, sep='')
        mask = cv2.inRange(hsv, lower, upper)

        # opening+closing to clean up (gives good results on ball size relative to image)
        ksize = 20
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        ksize = 5
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # find and display ball centroids with bounding boxes
        num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(mask)

        # Do not find more than two ( 1 for cue and black)
        found = 0
        possibleMatches = []
        for stat, centroid in zip(stats, centroids):
            # do not use centroid of whole-image component (ball is < 7000 area)
            if  stat[cv2.CC_STAT_AREA] < 15000:

                if colorlist[i] == 'white':  # cue ball
                    distances = np.array([10000.0])

                    for _, _, _, c in found_balls:  # make sure cue ball is not just part of a stripe ball
                        dist = np.linalg.norm(centroid - c)
                        if dist != 0.0:
                            distances = np.append(distances, [dist])

                    min = np.ndarray.min(distances, axis=0)
                    if min > 150.0:
                        possibleMatches.append((stat, centroid))

                else:
                    possibleMatches.append((stat, centroid))

        largest_stat = None
        largest_centroid = None
        secondl_stat = None
        secondl_centroid = None
        largest_area = 0
        secondl_area = 0
        if colorlist[i] == 'black':  # find black object closest to middle for 8 ball
            center = (width / 2, height / 2)
            ds = []
            min = 100000
            for stat, centroid in possibleMatches:
                dist = np.linalg.norm(centroid - center)
                if stat[cv2.CC_STAT_AREA] > 1000:
                    ds.append((dist, stat, centroid))
            for d, stat, c in ds:
                if d < min:
                    min = d
                    largest_centroid = c
                    largest_stat = stat

        else:  # for all other balls find stripe and solid by area
            for stat, centroid in possibleMatches:
                if stat[cv2.CC_STAT_AREA] > largest_area:
                    if largest_area > 0:
                        secondl_area = largest_area
                        secondl_stat = largest_stat
                        secondl_centroid = largest_centroid
                    largest_area = stat[cv2.CC_STAT_AREA]
                    largest_stat = stat
                    largest_centroid = centroid
                elif stat[cv2.CC_STAT_AREA] > secondl_area:
                    secondl_area = stat[cv2.CC_STAT_AREA]
                    secondl_stat = stat
                    secondl_centroid = centroid

        if largest_stat is not None:
            found += 1
            found_balls.append(('solid', colorlist[i], largest_stat, largest_centroid))
            x0 = largest_stat[cv2.CC_STAT_LEFT]
            y0 = largest_stat[cv2.CC_STAT_TOP]
            w = largest_stat[cv2.CC_STAT_WIDTH]
            h = largest_stat[cv2.CC_STAT_HEIGHT]
            img = cv2.rectangle(
                img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                color=(255, 255, 255), thickness=3)

        if secondl_stat is not None and colorlist[i] != 'white':
            found += 1
            found_balls.append(('striped', colorlist[i], secondl_stat, secondl_centroid))
            x0 = secondl_stat[cv2.CC_STAT_LEFT]
            y0 = secondl_stat[cv2.CC_STAT_TOP]
            w = secondl_stat[cv2.CC_STAT_WIDTH]
            h = secondl_stat[cv2.CC_STAT_HEIGHT]
            img = cv2.rectangle(
                img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                color=(255, 255, 255), thickness=3)

        create_named_window("mask", mask)
        cv2.imshow("mask", mask)
        # cv2.waitKey(0)

        wname = colorlist[i] + " found: " + str(found)
        create_named_window(wname, img)
        cv2.imshow(wname, img)
        cv2.waitKey(0)

    return found_balls
