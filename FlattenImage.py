import cv2.cv2

from imports import *
from miscFunctions import *


def orthoganize_image(image, points):
    height = image.shape[0]
    width = image.shape[1]
    ortho_points = np.array([
        # [x, y]
        [100, 100],  # top left
        [1000, 100],  # top right
        [1000, 600],  # bottom right
        [100, 600]],  # bottom left
        dtype="float32")
    perspective_matrix = cv2.getPerspectiveTransform(points, ortho_points)
    print(perspective_matrix)
    return cv2.warpPerspective(image, perspective_matrix, (width, height))


def flattenImage(img):
    corners = setCorners(img)
    ortho_img = orthoganize_image(img, corners)
    # TODO: crop ortho image correctly
    return ortho_img


# checking for white diamond 'keypoints'
def getkeypoints(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    lower_range = np.array([200, 200, 180])
    upper_range = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # opening+closing to clean up
    ksize = 10
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find and display found centroids with bounding boxes
    num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(mask)
    targets = []

    for stat, centroid in zip(stats, centroids):
        if (stat[cv2.CC_STAT_AREA] < 500 and stat[cv2.CC_STAT_AREA] > 20):  # do not use centroid if call, noise, etc
            x0 = stat[cv2.CC_STAT_LEFT]
            y0 = stat[cv2.CC_STAT_TOP]
            w = stat[cv2.CC_STAT_WIDTH]
            h = stat[cv2.CC_STAT_HEIGHT]
            targets.append(np.array([centroid[0], centroid[1]]))
            # print(centroid[0], centroid[1])
            img = cv2.rectangle(
                img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                color=(255, 0, 0), thickness=3)

    # finding colinear edge keypoints
    # TODO: check more than 3 colinear components

    # lines = []
    # dMin = 30
    # for x in range(0, 3):
    #     for i in range(0, len(targets)):
    #         for j in range(i+1, len(targets)):
    #             # Get the mid point between i,j.
    #             midPt = (targets[i] + targets[j])/2
    #             # Find another target that is closest to this midpoint.
    #             for k in range(0, len(targets)):
    #                 if k==i or k==j:
    #                     continue
    #                 d = np.linalg.norm(targets[k] - midPt)   # distance from midpoint
    #                 if d < dMin and np.linalg.norm(targets[j] - targets[i]) > 100:
    #                     line = np.array([targets[i], targets[j]], np.int32)
    #                     lines.append(line)
    #                     # dMin = d        # This is the minimum found so far; save it
    # for line in lines:
    #     img = cv2.circle(img, (line[0]), 10, (0, 0, 255), 3)
    #     img = cv2.circle(img, (line[1]), 10, (0, 0, 255), 3)
    #     img = cv2.line(img, line[0], line[1], (255, 255, 255), 10)
    #
    #
    # create_named_window("mask", mask)
    # cv2.imshow("mask", mask)
    #
    # create_named_window("img", img)
    # cv2.imshow("img", img)
    #
    # cv2.waitKey(0)
    return img


def setCorners(img):
    #click_points = []
    click_points = [(911, 984), (3064, 887), (3451, 1548), (319, 1641)]

    if len(click_points) != 0:
        return np.array(click_points, dtype="float32")

    create_named_window("Pool table Corners", img)
    cv2.imshow("Pool table Corners", img)
    cv2.setMouseCallback("Pool table Corners", on_mouse=get_xy, param=("Pool table Corners", img, click_points))

    print("Click on the center of each corner pocket.  Hit ESC to finish.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break
    print("clicked points:", click_points)  # Print points to the console
    return np.array(click_points, dtype="float32")


def Houghwarp(points, img):
    # short/long side points
    s = np.sum(points, axis=1);
    l = np.diff(points, axis=1);
    corners = np.reshape([points[np.argmin(s)], points[np.argmin(l)], points[np.argmax(s)], points[np.argmax(l)]],
                         (4, 2))
    (tl, tr, br, bl) = corners
    # trapezoid/perspective width
    width_top = np.sqrt((tl[0] - tr[0]) ** 2 + (tl[1] - tr[1]) ** 2)
    width_bottom = np.sqrt((bl[0] - br[0]) ** 2 + (bl[1] - br[1]) ** 2)
    max_width = max(int(width_top), int(width_bottom))
    # trapezoid/perspective height
    height_left = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
    height_right = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
    max_height = max(int(height_left), int(height_right))
    # transform
    to_points = np.array([[0, 0], [max_width + 1, 0], [max_width + 1, max_height + 1], [0, max_height + 1]],
                         dtype="float32")
    transMtx = cv2.getPerspectiveTransform(corners, to_points)
    img = cv2.warpPerspective(img, transMtx, (max_width, max_height))

    create_named_window("houghwarp", img)
    cv2.imshow("houghwarp", img)
    cv2.waitKey(0)
    return img


def houghlines(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 70, apertureSize=3)
    minLineLength = 800
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=50)
    a, b, c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    return img
