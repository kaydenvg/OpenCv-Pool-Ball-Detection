from imports import *

def nothing(x):
    pass

def create_named_window(window_name, image):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    h = image.shape[0]  # image height
    w = image.shape[1]  # image width
    WIN_MAX_SIZE = 1000
    if max(w, h) > WIN_MAX_SIZE:
        scale = WIN_MAX_SIZE / max(w, h)
    else:
        scale = 1
    cv2.resizeWindow(winname=window_name, width=int(w * scale), height=int(h * scale))

def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        window_name, image, point_list = param  # Unpack parameters
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.putText(image, str(len(point_list)), org=(x, y - 15), color=(0, 0, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=2)
        cv2.imshow(window_name, image)
        point_list.append((x, y))

def colorPicker(filename, colorlist=None):
    """
    opens an image window, returns a list of colors in order which they are clicked on in the image
    :param filename: image file to open
    :param colorlist: color list variable to write clicked colors to
    """
    img = cv2.imread(filename)
    create_named_window(filename, img)
    cv2.imshow(filename, img)
    cv2.setMouseCallback(filename, on_mouse=get_color_on_click, param=(filename, img, colorlist))
    print("Click on points to get RGB value.  Hit ESC to exit.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break

def get_color_on_click(event, x, y, flags, param):
    """
    on-click event for colorPicker function
    :param event:
    :param x: image x coord
    :param y: image y coord
    :param flags:
    :param param: list of params to be unpacked, includes:
        window_name to display to,
        image to display,
        list of colors to write to
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        window_name, image, colorlist = param  # Unpack parameters
        # cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(255,255,255),thickness=2) # optionally view color pick point (will overlap and cause white if clicked)
        color = tuple(reversed(image[y, x]))
        cv2.imshow(window_name, image)
        print("RGB Value at ({},{}):{} ".format(x, y, color))
        colorlist.append(color)
