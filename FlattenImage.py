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
    #print(perspective_matrix)
    return cv2.warpPerspective(image, perspective_matrix, (width, height))

def flattenImage(filename):
    img = cv2.imread(filename)
    corners = getCorners(img)
    ortho_img = orthoganize_image(img, corners)
    # TODO: crop ortho image
    return ortho_img

def getCorners(img):
    # click_points = []
    click_points = [(823, 867), (3242, 907), (3746, 2125), (298, 2081)]

    if len(click_points) != 0:
        return np.array(click_points, dtype = "float32")

    create_named_window("Pool table Corners", img)
    cv2.imshow("Pool table Corners", img)
    cv2.setMouseCallback("Pool table Corners", on_mouse=get_xy, param=("Pool table Corners", img, click_points))

    print("Click on the center of each corner pocket.  Hit ESC to finish.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break
    print("clicked points:", click_points)      # Print points to the console
    return np.array(click_points, dtype = "float32")