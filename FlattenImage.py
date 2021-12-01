import cv2.cv2

from imports import *
from miscFunctions import *
def orthoganize_image(image, points):
    height = image.shape[0]
    width = image.shape[1]
    ortho_points = np.array([
        #[x, y]
        [100, 100],     #top left
        [1000, 100],   # top right
        [1000, 600], # bottom right
        [100, 600 ]], # bottom left
        dtype = "float32")
    perspective_matrix = cv2.getPerspectiveTransform(points, ortho_points)
    print(perspective_matrix)
    return cv2.warpPerspective(image, perspective_matrix, (width, height))

def flattenImage(img):
    corners = getCorners(img)
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
    dMin = 1e9

    for stat, centroid in zip(stats, centroids):
        if (stat[cv2.CC_STAT_AREA] < 500 and stat[cv2.CC_STAT_AREA] > 100):  # do not use centroid if call, noise, etc
            x0 = stat[cv2.CC_STAT_LEFT]
            y0 = stat[cv2.CC_STAT_TOP]
            w = stat[cv2.CC_STAT_WIDTH]
            h = stat[cv2.CC_STAT_HEIGHT]
            targets.append(np.array([centroid[0], centroid[1]]))
            # print(centroid[0], centroid[1])
            img = cv2.rectangle(
                img=img, pt1=(x0, y0), pt2=(x0 + w, y0 + h),
                color=(255, 0, 0), thickness=3)

    #finding colinear edge keypoints
    #TODO: check more than 3 colinear components
    for i in range(0, len(targets)):
        for j in range(i+1, len(targets)):
            # Get the mid point between i,j.
            midPt = (targets[i] + targets[j])/2

            # Find another target that is closest to this midpoint.
            for k in range(0, len(targets)):
                if k==i or k==j:
                    continue
                d = np.linalg.norm(targets[k] - midPt)   # distance from midpoint
                if d < dMin:
                    dMin = d        # This is the minimum found so far; save it
                    i0 = targets[i]
                    i1 = targets[k]
                    i2 = targets[j]

    #TODO: optionally display keypoints/lines around edge
    img = cv2.circle(img, (int(i0[0]), int(i0[1])), 10, (0, 0, 255), 3)
    img = cv2.circle(img, (int(i1[0]), int(i1[1])), 10, (0, 0, 255), 3)
    img = cv2.circle(img, (int(i2[0]), int(i2[1])), 10, (0, 0, 255), 3)


    create_named_window("mask", mask)
    cv2.imshow("mask", mask)

    create_named_window("img", img)
    cv2.imshow("img", img)

    cv2.waitKey(0)


def getCorners(img):
    click_points  = []
    create_named_window("Pool table Corners", img)
    cv2.imshow("Pool table Corners", img)
    cv2.setMouseCallback("Pool table Corners", on_mouse=get_xy, param=("Pool table Corners", img, click_points))

    print("Click on the center of each corner pocket.  Hit ESC to finish.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break
    print("clicked points:", click_points)      # Print points to the console
    return np.array(click_points, dtype = "float32")