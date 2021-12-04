from imports import *
from FindBalls import *
from miscFunctions import *
from FlattenImage import *
from findShot import *

if __name__ == '__main__':
    file = 'table2.png'
    ortho = flattenImage(file)

    # setImageThresholds()
    cv2.imshow("ortho", ortho)
    cv2.waitKey(0)
    foundballs = findBalls(ortho)

    # create_named_window("found balls image", foundballs)
    cv2.imshow("found balls image", foundballs)

    cv2.waitKey(0)
