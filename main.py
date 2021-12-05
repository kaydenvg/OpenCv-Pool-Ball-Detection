from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *

if __name__ == '__main__':
    file = 'IMG_1292.JPG'
    img = cv2.imread(file)
    # flattenImage(img)
    ortho = Houghwarp(setCorners(img), img)
    # colorPicker(ortho)
    #
    #
    findBalls(ortho)
    # setImageThresholds(ortho)
    #
    cv2.waitKey(0)



