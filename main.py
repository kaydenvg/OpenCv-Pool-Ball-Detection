from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *

if __name__ == '__main__':
    file = 'table1.png'
    img = cv2.imread(file)
    getkeypoints(img)
    # ortho = flattenImage(file)
    #
    #
    # foundballs = findBalls(ortho)
    #
    # # create_named_window("found balls image", foundballs)
    # cv2.imshow("found balls image", foundballs)
    # cv2.waitKey(0)



