from imports import *
from miscFunctions import *
import math
def getAllShots(img, team, b_positions):
    solid_b_loc = []
    cueball_loc = []
    for team, color, stat, center in b_positions:
        center = np.array(center, np.int32)
        if color == 'white':
            #TODO: get center of cue ball
            cueball_loc = center
            print(cueball_loc)
        if team == 'solid' and stat is not None \
                and color != 'white'\
                and color != 'black':
            #TODO get center of each ball/team of ball
            solid_b_loc.append(center)


    #TODO: get pocket locations
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
    distances = []
    for pocket in pocketLocs:
        img = cv2.circle(img, np.array(pocket, np.int32), 10, (0, 0, 255), 3)
        for ball_loc in solid_b_loc:
            line1 = np.array([ball_loc, cueball_loc], np.int32)
            line2 = np.array([ball_loc, pocket], np.int32)
            angle = ang(line1, line2)
            if angle > 100:
                lines1.append(line1)
                lines2.append(line2)
                angles.append(180 - angle)
                distances.append(np.linalg.norm(line1[1] - line1[0]) + np.linalg.norm(line2[1] - line2[0]))

    # # show all shots
    for line1, line2 in zip(lines1, lines2):
        img = cv2.circle(img, (line1[0]), 10, (0, 0, 255), 3)
        img = cv2.circle(img, (line1[1]), 10, (0, 0, 255), 3)
        img = cv2.line(img, line1[0], line1[1], (0, 255, 255), 10)

        img = cv2.circle(img, (line2[0]), 10, (0, 0, 255), 3)
        img = cv2.circle(img, (line2[1]), 10, (0, 0, 255), 3)
        img = cv2.line(img, line2[0], line2[1], (255, 255, 255), 10)

        angle = ang(line1, line2)
        # print("angle", angle)

        # create_named_window("shot", img)
        # cv2.imshow("shot", img)
        # cv2.waitKey(0)

    return lines1, lines2, angles, distances

def getBestShot(img, lines1, lines2, angles, distances, priority='distance'):
    # display line with lowest shot angle
    assert priority in ['distance', 'angle']
    if priority =='distance':
        bestshotidx = np.argmin(distances)
    else:
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