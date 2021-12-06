from imports import *
from miscFunctions import *
import math
def getAllShots(img, team, b_positions):
    shot_thresh = .5
    solid_b_loc = []
    cueball_loc = []
    for team, color, stat, centroid in b_positions:
        if color == 'white':
            cueball_loc = stat[:2]
        if team == 'solid' and stat is not None and color != 'white':
            solid_b_loc.append(stat[:2])


    pocketLocs = [(50, 50),
                  (50, img.shape[0] - 50),
                  (img.shape[1] - 50, img.shape[0] - 50),
                  (img.shape[1] - 50, 50),
                  #edge pockets:
                  (img.shape[1]/2, 50),
                  (img.shape[1] / 2, img.shape[0] - 50),
                  ]
    lines1 = []
    lines2 = []
    angles = []
    for pocket in pocketLocs:
        for ball_loc in solid_b_loc:
            line1 = np.array([ball_loc, cueball_loc], np.int32)
            line2 = np.array([ball_loc, pocket], np.int32)
            angle = ang(line1, line2)
            if angle > 100:
                lines1.append(line1)
                lines2.append(line2)
                angles.append(180 - angle)

    # # show all shots
    # for line1, line2 in zip(lines1, lines2):
    #     img = cv2.circle(img, (line1[0]), 10, (0, 0, 255), 3)
    #     img = cv2.circle(img, (line1[1]), 10, (0, 0, 255), 3)
    #     img = cv2.line(img, line1[0], line1[1], (0, 255, 255), 10)
    #
    #     img = cv2.circle(img, (line2[0]), 10, (0, 0, 255), 3)
    #     img = cv2.circle(img, (line2[1]), 10, (0, 0, 255), 3)
    #     img = cv2.line(img, line2[0], line2[1], (255, 255, 255), 10)
    #
    #     angle = ang(line1, line2)
    #     print("angle", angle)
    #
    #     create_named_window("shot", img)
    #     cv2.imshow("shot", img)
    #     cv2.waitKey(0)

    return lines1, lines2, angles

def getBestShot(img, lines1, lines2, angles):
    # display line with lowest shot angle
    bestshotidx = np.argmin(angles)
    # print("best:", bestshotidx, angles[bestshotidx])
    # print(lines2)
    # print(lines2[bestshotidx][0])
    img = cv2.line(img, lines1[bestshotidx][0], lines1[bestshotidx][1], (0, 255, 255), 10)
    img = cv2.line(img, lines2[bestshotidx][0], lines2[bestshotidx][1], (255, 255, 255), 10)
    img = cv2.circle(img, (lines2[bestshotidx][0]), 10, (0, 0, 255), 3)

    # create_named_window("shot", img)
    # cv2.imshow("shot", img)
    # cv2.waitKey(0)

    return img

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg