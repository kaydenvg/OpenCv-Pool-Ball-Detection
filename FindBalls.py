import cv2.cv2

from imports import *
from miscFunctions import *


def setImageThresholds():
    # set HSV thresholds HUE:0-179 | SATURATION/VALUE:0-255
    low_thresholds = [0, 0, 0]
    high_thresholds = [179, 255, 255]

    # import image, convert to hsv
    # filename = str(input("enter a file name:"))
    filename = 'table2.png'
    bgr_img = cv2.imread(filename)

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


def findBalls(img):
    """
    Finds each color of pool ball in an image file
    :param filename: image file name - string

    return list [ tuple (colorname, ballstats) ]
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    found_balls = []

    # Poolball color values
    colorlist = ['yellow', 'blue', 'red', 'purple', 'orange', 'green', 'burgundy', 'black', 'white']
    hue_ranges = [(15, 35), (105, 120), (170, 177), (165, 179), (3, 7), (30, 60), (0, 4), (0, 179), (0, 179)]
    sat_ranges = [(150, 255), (0, 255), (138, 255), (70, 125), (166, 210), (43, 110), (100, 160), (0, 50), (50, 150)]
    val_ranges = [(150, 255), (60, 255), (200, 255), (80, 255), (230, 255), (37, 150), (100, 255), (0, 100), (245, 255)]

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

    for i in range(len(colorlist)):
        hLow, hHigh = hue_ranges[i]
        sLow, sHigh = sat_ranges[i]
        vLow, vHigh = val_ranges[i]

        lower = (hLow, sLow, vLow)
        upper = (hHigh, sHigh, vHigh)

        print(colorlist[i] + ' threshold: L=', lower, ' H=', upper, sep='')
        mask = cv2.inRange(hsv, lower, upper)

        # opening+closing to clean up (gives good results on ball size relative to image)
        ksize = 25
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        ksize = 15
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # find and display ball centroids with bounding boxes
        num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(mask)

        # Do not find more than two ( 1 for cue and black)
        found = 0
        possibleMatches = []
        for stat, centroid in zip(stats, centroids):
            # do not use centroid of whole-image component (ball is < 4000 area)
            if 7000 > stat[cv2.CC_STAT_AREA] > 250:
                # x0 = stat[cv2.CC_STAT_LEFT]
                # y0 = stat[cv2.CC_STAT_TOP]
                # w = stat[cv2.CC_STAT_WIDTH]
                # h = stat[cv2.CC_STAT_HEIGHT]
                # img = cv2.rectangle(
                #     img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                #     color=(255, 255, 255), thickness=3)

                # img = cv2.circle(img=img, center=(int(centroid[0]), int(centroid[1])), radius=stat[cv2.CC_STAT_WIDTH],
                #                  color=(255, 255, 255), thickness=3)
                # print(centroid)
                found += 1
                possibleMatches.append(stat)

        print(found)
        # find largest area
        largest_stat = None
        secondl_stat = None
        largest_area = 0
        secondl_area = 0
        for stat in possibleMatches:
            if stat[cv2.CC_STAT_AREA] > largest_area:
                if largest_area > 0:
                    secondl_area = largest_area
                    secondl_stat = largest_stat
                largest_area = stat[cv2.CC_STAT_AREA]
                largest_stat = stat
            elif found > 1 and stat[cv2.CC_STAT_AREA] > secondl_area:
                secondl_area = stat[cv2.CC_STAT_AREA]
                secondl_stat = stat

        found_balls.append(('solid', colorlist[i], largest_stat))
        x0 = largest_stat[cv2.CC_STAT_LEFT]
        y0 = largest_stat[cv2.CC_STAT_TOP]
        w = largest_stat[cv2.CC_STAT_WIDTH]
        h = largest_stat[cv2.CC_STAT_HEIGHT]
        img = cv2.rectangle(
            img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
            color=(255, 255, 255), thickness=3)

        if secondl_stat is not None and i < len(colorlist) - 2:
            found_balls.append(('striped', colorlist[i], secondl_stat))
            x0 = secondl_stat[cv2.CC_STAT_LEFT]
            y0 = secondl_stat[cv2.CC_STAT_TOP]
            w = secondl_stat[cv2.CC_STAT_WIDTH]
            h = secondl_stat[cv2.CC_STAT_HEIGHT]
            img = cv2.rectangle(
                img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                color=(255, 255, 255), thickness=3)

        create_named_window("mask", mask)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)

        wname = colorlist[i] + " found: " + str(found)
        create_named_window(wname, img)
        cv2.imshow(wname, img)
        cv2.waitKey(0)

    return found_balls
