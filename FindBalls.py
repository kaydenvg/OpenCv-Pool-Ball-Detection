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
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Poolball color values
    colorlist = ['yellow', 'blue', 'red', 'purple', 'orange', 'green', 'burgundy', 'black', 'white']
    hue_ranges = [(15, 45), (75, 120), (172, 179), (165, 179), (0, 15), (45, 75), (170, 179), (0, 35), (150, 179)]
    sat_ranges = [(150, 255), (0, 120), (138, 255), (70, 125), (166, 255), (43, 110)]
    val_ranges = [(150, 255), (60, 255), (70, 255), (80, 255), (245, 255), (37, 150)]

    table_range = [(80, 170, 100), (120, 221, 172)]

    # table_mask = cv2.inRange(hsv, table_range[0], table_range[1])
    # cv2.imshow("table mask", table_mask)
    # cv2.waitKey(0)

    for i in range(len(colorlist)):
        hLow, hHigh = hue_ranges[i]
        sLow, sHigh = sat_ranges[i]
        vLow, vHigh = val_ranges[i]

        lower = (hLow, sLow, vLow)
        upper = (hHigh, sHigh, vHigh)

        print(colorlist[i] + ' threshold: L=', lower, 'H=', upper, sep='')
        mask = cv2.inRange(hsv, lower, upper)

        # opening+closing to clean up (gives good results on ball size relative to image)
        ksize = 25
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        ksize = 10
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # find and display ball centroids with bounding boxes
        num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(mask)

        for stat, centroid in zip(stats, centroids):
            if stat[cv2.CC_STAT_AREA] < 5000:  # do not use centroid of whole-image component (ball is < 4000 area)
                x0 = stat[cv2.CC_STAT_LEFT]
                y0 = stat[cv2.CC_STAT_TOP]
                w = stat[cv2.CC_STAT_WIDTH]
                h = stat[cv2.CC_STAT_HEIGHT]
                img = cv2.rectangle(
                    img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                    color=(255, 255, 255), thickness=3)

        create_named_window("mask", mask)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)

        create_named_window("img", img)
        cv2.imshow("img", img)
        cv2.waitKey(0)

    return img
