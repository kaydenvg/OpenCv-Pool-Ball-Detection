from imports import *
from miscFunctions import *

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

def findBalls(img):
    """
    Finds each color of pool ball in an image file
    :param filename: image file name - string
    """
    # colorlist = []
    # colorPicker(filename, colorlist=colorlist)
    # print(colorlist)

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # orange ranges:
    lower_range = np.array([230, 85, 60])
    upper_range = np.array([255, 120, 75])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    # TODO: loop through all colored balls, currently only orange

    #opening+closing to clean up (gives good results on ball size relative to image)
    ksize = 25
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    ksize = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    #find and display ball centroids with bounding boxes
    num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(mask)

    for stat, centroid in zip(stats, centroids):
        if(stat[cv2.CC_STAT_AREA] < 5000): # do not use centroid of whole-image component (ball is < 4000 area)
            x0 = stat[cv2.CC_STAT_LEFT]
            y0 = stat[cv2.CC_STAT_TOP]
            w = stat[cv2.CC_STAT_WIDTH]
            h = stat[cv2.CC_STAT_HEIGHT]
            img = cv2.rectangle(
            img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
            color=(255, 255, 255), thickness=3)

    # create_named_window("mask", mask)
    # cv2.imshow("mask", mask)
    # cv2.waitKey(0)

    # create_named_window("img", img)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    return img